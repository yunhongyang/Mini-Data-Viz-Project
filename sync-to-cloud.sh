

# SYNC LOCAL VERSION OF WEBSITE TO GU-DOMAINS SERVER
rsync -alvr --delete Mini-Data-Viz-Project yunhong1@gtown.reclaimhosting.com:/home/yunhong1/public_html/
rsync -alvr --delete Code yunhong1@gtown.reclaimhosting.com:/home/yunhong1/public_html/
rsync -alvr --delete 2023-04-14-job-search yunhong1@gtown.reclaimhosting.com:/home/yunhong1/public_html/

# PUSH GIT REPO TO THE CLOUD FOR BACKUP
DATE=$(date +"DATE-%Y-%m-%d-TIME-%H-%M-%S")
message="GITHUB-UPLOAD:$DATE";
echo "commit message = "$message; 
git add ./; 
git commit -m $message; 
git push
