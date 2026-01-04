from flask_store import create_app
POSTGRES = {
   'user':'postgres',
   'password':'test',
   'db':'mystore',
   'host':'localhost',
   'port':'5432',
}

# app = create_app()
app = create_app(POSTGRES)

if __name__=='__main__':
    app.run(debug=True)