echo "old docker processes die..."
docker compose rm -fs

echo "...so that new ones may live" 
docker compose up --build -d 
