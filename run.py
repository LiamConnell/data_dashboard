from app import app
if __name__ == '__main__':
    app.run(host=app.config.get("HOST", "ec2-52-90-86-30.compute-1.amazonaws.com"),
        port=app.config.get("PORT", 8888),
        debug=True)

