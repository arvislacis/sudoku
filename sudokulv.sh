#!/bin/bash
# (CC BY-SA) 2013 Arvis Lācis (@arvislacis)

cels=/opt/sudokulv
ver="v1.1"

if [[ -f /usr/bin/apt-get ]]; then
	os="Debian"
elif [[ -f /usr/bin/yum ]]; then
	os="Red Hat"
else
	if [[ -f /usr/bin/pacman ]]; then
		os="Arch Linux"
	else
		os="nezināma"
	fi
fi

if [[ "$os" == "nezināma" ]]; then
	echo "Atvainojiet, jūsu izmantotā sitēma pašlaik netiek atbalstīta, sazinieties ar skripta izstrādātāju!"
	zenity --error --title="Neatbalstīta sistēma" --text="<b><span color=\"red\">Atvainojiet, jūsu izmantotā sitēma pašlaik netiek atbalstīta, sazinieties ar skripta izstrādātāju!</span></b>"
	exit 1
fi

case $1 in
	"")
		if [[ $UID -eq 0 ]]; then
			if [[ -f /usr/bin/sudokulv ]]; then
				darbiba=$(zenity --list --title="Izvēlieties darbību" --text="Spēle <b>Sudoku $ver</b> jau ir instalēta jūsu sistēmā." --column="Veicamā darbība" "Palaist spēli" "Atjaunināt spēles datnes" "Atinstalēt spēli" "Palīdzība" "Par...")
				
				case $darbiba in
					"Palaist spēli")
						sudokulv --start
						exit 1;;
					"Atjaunināt spēles datnes")
						if [[ "$0" == "/usr/bin/sudokulv" ]]; then
							zenity --error --title="Nevar atjaunināt" --text="<b><span color=\"red\">Spēles datņu atjaunināšana iespējama tikai no instalācijas skripta (sudokulv.sh).</span></b>"
							exit 1
						fi;;
					"Atinstalēt spēli")
						sudokulv --remove
						exit 1;;
					"Palīdzība")
						sudokulv --help
						exit 1;;
					"Par...")
						sudokulv --about
						exit 1;;
				esac
			fi
			
			if [[ ! -f /usr/bin/zenity ]]; then
				(case $os in
					"Debian")
						apt-get install zenity;;
					"Red Hat")
						yum install zenity;;
					"Arch Linux")
						pacman -S zenity;;
				esac) | zenity --progress --title="Zenity pakotnes instalēšana" --text="Uzgaidiet, notiek <b>Zenity</b> pakotnes instalēšana." --auto-close --pulsate
			fi
			
			zenity --info --title="Sudoku instalēšanas rīks v0.8.2" --text="Esiet sveicināti spēles <b>Sudoku $ver</b> instalēšanas rīkā.\n\nNospiediet <b>OK</b>, lai turpinātu instalēšanas procesu."
			
			if [[ ! -f /usr/bin/python ]]; then
				(case $os in
					"Debian")
						apt-get install python;;
					"Red Hat")
						yum install python;;
					"Arch Linux")
						pacman -S python2;;
				esac) | zenity --progress --title="Python pakotnes instalēšana" --text="Uzgaidiet, notiek <b>Python</b> pakotnes instalēšana." --auto-close --pulsate
			fi
			
			if [[ ! (( -d /usr/lib/python2.7/dist-packages/pygame ) || ( -d /usr/lib64/python2.7/dist-packages/pygame ) || ( -d /usr/lib/python2.7/site-packages/pygame ) || ( -d /usr/lib64/python2.7/site-packages/pygame )) ]]; then
				(case $os in
					"Debian")
						apt-get install python-pygame;;
					"Red Hat")
						yum install pygame;;
					"Arch Linux")
						pacman -S python2-pygame;;
				esac) | zenity --progress --title="PyGame pakotnes instalēšana" --text="Uzgaidiet, notiek <b>PyGame</b> pakotnes instalēšana." --auto-close --pulsate
			fi
			
			(mkdir -p $cels
			cp -fu ./sudokulv/sudokulv.pyw $cels
			cp -rfu ./sudokulv/images $cels
			cp -rfu ./sudokulv/fonts $cels
			cp -fu ./sudokulv/sudokulv /usr/bin
			cp -fu ./sudokulv/sudokulv.desktop /usr/share/applications) | zenity --progress --title="Datņu kopēšana" --text="Uzgaidiet, notiek <b>Sudoku $ver</b> datņu kopēšana." --auto-close --pulsate
			
			if [[ -f /usr/bin/sudokulv ]]; then
				zenity --question --title="Instalēšana pabeigta" --text="<b>Sudoku $ver</b> instalēšana veiksmīgi pabeigta!\nVai vēlaties tagad palaist spēli?"
				case $? in
					0)
						python /opt/sudokulv/sudokulv.pyw;;
					1)
						exit 1;;
				esac
			else
				zenity --error --title="Kļūda instalēšanā" --text="<b><span color=\"red\">Atvainojiet, instalēšanas procesā radās kļūda. Mēģiniet palaist instalēšanas skriptu vēlreiz vai arī sazinieties ar skripta izstrādātāju.</span></b>"
			fi
		else
			if [[ "$0" == "/usr/bin/sudokulv" ]]; then
				sudokulv --start
				exit 1
			fi
			
			if [[ ! -f /usr/bin/gksu ]]; then
				echo "Lai instalētu Sudoku $ver, nepieciešamas sudo piekļuves tiesības."
				echo "Terminālī izpildiet sekojošu komandu: sudo ./sudokulv.sh."
				echo
				echo "Ja izmantojiet Debian (Ubuntu, Linux Mint...) vai Arch Linux bāzētu sistēmu,"
				echo "varat instalēt pakotni gksu un pēc tam atkārtoti palaidiet šo skriptu."
				zenity --error --title="Nepieciešamas sudo piekļuves tiesības" --text="<span color=\"red\">Lai instalētu spēli, nepieciešamas sudo piekļuves tiesības.\nTerminālī izpildiet sekojošu komandu: <b>sudo ./sudokulv.sh</b>.\n\nJa izmantojiet Debian (Ubuntu, Linux Mint...) vai Arch Linux bāzētu sistēmu, varat instalēt pakotni <b>gksu</b> un pēc tam atkārtoti palaidiet šo skriptu.</span>"
				exit 1
			fi
			
			gksu "bash" $0 $@ --message="Sudoku $ver instalēšanai ir nepieciešamas sudo piekļuves tiesības, lai ierakstītu datus /opt, /usr/bin un /usr/share/applications direktorijās. Lūdzu, zemāk esošajā laukā ievadiet sudo piekļuves paroli un nospiediet pogu OK, lai turpinātu instalēšanu."
		fi;;
		
	--run|--start|--palaist|--sakt)
		python /opt/sudokulv/sudokulv.pyw;;
		
	-a|--about|--par)
		zenity --info --title="Sudoku $ver" --text="<b>(CC BY-SA) Aija Trimdale</b>\nE-pasts: aija.trimdale@r6vsk.lv";;
		
	-h|--help|--palidziba)
		zenity --info --title="Sudoku $ver palīdzība" --text="Terminālī iespējams izmantot šādas komandas:\n<b>sudokulv --about</b>\t- vispārīgās informācijas parādīšana\n<b>sudokulv --help</b>\t- šī palīdzības loga parādīšana\n<b>sudokulv --start</b>\t- spēles palaišana\n\nAr sudo piekļuves tiesībām papildus iespējams izpildīt šādu komandu:\n<b>sudo sudokulv --remove</b>\t- spēles atinstalēšana";;
		
	-r|--remove|--uninstall|--atinstalet|--nonemt)
		if [[ $UID -eq 0 ]]; then
			(rm -rf /opt/sudokulv
			rm -f /usr/bin/sudokulv
			rm -f /usr/share/applications/sudokulv.desktop) |  zenity --progress --title="Datņu dzēšana" --text="Uzgaidiet, notiek <b>Sudoku $ver</b> datņu dzēšana." --auto-close --pulsate
			zenity --info --title="Atinstalēšana pabeigta" --text="<b>Sudoku $ver</b> atinstalēšana veiksmīgi pabeigta!"
		else
			zenity --error --title="Nepieciešamas sudo piekļuves tiesības" --text="<span color=\"red\">Lai atinstalētu spēli, nepieciešamas sudo piekļuves tiesības.\nTerminālī izpildiet sekojošu komandu: <b>sudo sudokulv --remove</b>.</span>"
		fi;;
esac