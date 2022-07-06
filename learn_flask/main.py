from website import create_app

app = create_app()

if __name__=='__main__':
# in this if statement, codes executed when only this file executed not imported
    app.run()
    
    