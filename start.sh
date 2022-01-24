echo "Repo Klonlanıyor..."
git clone https://github.com/BirBeyfendi/magnetarvc.git /VC_PLAYER
cd /VC_PLAYER
pip3 install -U -r requirements.txt
echo "Bot Başlatılıyor..."
python3 bot.py
