

# SYNC LOCAL VERSION OF WEBSITE TO GU-DOMAINS SERVER
#rsync -alvr --delete 501-project-website yunhong1@gtown.reclaimhosting.com:/home/yunhong1/public_html/

# PUSH GIT REPO TO THE CLOUD FOR BACKUP
DATE=$(date +"DATE-%Y-%m-%d-TIME-%H-%M-%S")
message="GITHUB-UPLOAD:$DATE";
echo "commit message = "$message; 
git add ./; 
git commit -m $message; 
git push
