source activate $ENV

echo "running Data Load" 
python src/db/db_conn.py
echo "starting server" 
python src/server.py 