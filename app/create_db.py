from app4 import app, db, Player, Review

# Player data for database
players = [
    { "name": "Viktor Gyokeres", "price": 95600000, "short_description": "World's best striker", 
     "long_description": """A powerful, high-intensity centre-forward who combines physical strength with impressive mobility. 
     Excellent at driving forward with the ball and attacking space behind defences. Strong finisher inside the box but also
     capable of creating chances through hold-up play and link-up runs. Brings aggression, pressing energy, and a relentless
     work rate to the front line.""", "image": "gyokeres.webp", "environmental_impact": 8 },
    
    { "name": "Bryan Mbeumo", "price": 80000000, "short_description": "Slow winger", "long_description" : """A versatile forward known for his work rate and intelligent movement, 
     Bryan Mbeumo plays a key role in Manchester United’s attacking system. While not the quickest winger, he makes up for it with sharp positioning, 
     link-up play, and a strong left foot. He consistently contributes with goals and assists, often drifting centrally to create chances and support the striker.""", 
     "image": "mbuemo.webp", "environmental_impact": 4 },
    
    { "name": "Jean-Philippe Mateta", "price": 40000000, "short_description": "There ain't no striker better", "long_description" : """A physically dominant striker with a real eye 
     for goal, Jean-Philippe Mateta thrives as a focal point in attack. His strength allows him to hold up play effectively, while his finishing inside the box makes him a constant 
     threat. Whether it's with his feet or in the air, he has the ability to turn half-chances into goals and lead the line with confidence.""", 
     "image": "mateta.webp", "environmental_impact": 6 },
    
    { "name": "Harry Wilson", "price": 25600000, "short_description": "Welsh winger", "long_description" : """A technically gifted winger with a wand of a left foot, Harry Wilson is known 
     for his creativity and set-piece ability. The Welsh international can unlock defences with precise passes and dangerous crosses, while also posing a goal threat from distance. His 
     vision and technique make him a valuable attacking outlet on the wing.""", "image": "wilson.webp", "environmental_impact": 2 },
    
    { "name": "Erling Haaland", "price": 200000000, "short_description": "Wishes he was Gyokeres", "long_description" : """One of the most prolific strikers in world football, Erling Haaland 
     combines incredible pace, strength, and clinical finishing. His movement in the box is elite, allowing him to consistently find space and convert chances with ruthless efficiency. A 
     nightmare for defenders, he has redefined goalscoring standards with his consistency and physical dominance.""", "image": "haaland.webp", "environmental_impact": 10},
    
    { "name": "Mohammed Salah", "price": 31500000, "short_description": "The Egyptian King", "long_description" : """A dynamic forward with exceptional pace and a lethal left foot, 
     Mohamed Salah is a constant threat from the right wing. His ability to cut inside and finish with precision makes him one of the most reliable goalscorers in the game. A nightmare 
     for defenders, he combines sharp movement and clinical finishing to consistently deliver at the highest level.""", "image": "salah.webp", "environmental_impact": 7}
]

with app.app_context():
    # Resets database
    db.drop_all()
    db.create_all()   
    
    # Inserts players into database
    for p in players:
        new_player = Player(
            name=p["name"],
            price=p["price"],
            short_description=p["short_description"],
            long_description=p["long_description"],
            image=p["image"],
            environmental_impact=p["environmental_impact"]
        )
        db.session.add(new_player)

    db.session.commit()
    print("Database created and players added!") 