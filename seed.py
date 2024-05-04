from models import User, Feedback, db
from app import app

#create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

u1=User.register("Apop","carrot","apop@gmail.com","Michael", "Ellis")
u2=User.register("Pikachu","lightening","pikachu@gmail.com","Pikachu", "Ketchum")
u3=User.register("Zapdos","electric","zapdos@gmail.com","Zapdos", "lighteninglegendary")
u4=User.register("Moltres","molten","moltres@gmail.com","Moltres", "Firelegendary")
u5=User.register("Gengar","ghostboy","gengar@gmail.com","Gengar", "FastestOGPokemon")
u6=User.register("Mewtwo","pyschic","mewtwo@gmail.com","Mewtwo", "Masterball")

with app.app_context():
    db.session.add_all([u1,u2,u3,u4,u5,u6])
    db.session.commit()

fb1=Feedback(title="Hey friend", content="I'm not your friend buddy", username="Apop")
fb2=Feedback(title="Hey buddy", content="I'm not your buddy guy", username="Apop")
fb3=Feedback(title="Hey guy", content="I'm not your guy friend", username="Apop")
fb4=Feedback(title="Hey friend", content="I'm not your friend buddy", username="Apop")
fb5=Feedback(title="Hey Dude", content="Was a TV show on nickelodeon in the 1990's", username="Pikachu")
fb6=Feedback(title="You need to tag pokemon with types dude", content="as stated", username="Zapdos")
fb7=Feedback(title="Pokemon types help you learn about their attributes", content="like maybe they're a grass type and shouldn't come into contact with fire", username="Moltres")
fb8=Feedback(title="IM THE FASTEST", content=" In the first 3 pokemon games realeased for gameboy gengar was the fastest pokemon! This means he was always guaranteed to go first", username="Gengar")
fb9=Feedback(title="MEWTWO", content="I was created in a a lab. My suggestion to you is.....release me.....now.......!", username="Mewtwo")

with app.app_context():
    db.session.add_all([fb1,fb2,fb3,fb4,fb5,fb6,fb7,fb8,fb9])
    db.session.commit()