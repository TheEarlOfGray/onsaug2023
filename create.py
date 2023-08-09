from app import db, app, Owner, Car, bcrypt


with app.app_context():
    db.drop_all()
    db.create_all()

    testuser = Owner(first_name="earl", last_name="Gray")
    db.session.add(testuser)
    db.session.commit()

    testcar = Car(num_plate='bf7 h8w', ownerbr=testuser)
    db.session.add(testcar)
    db.session.commit()
    testcar2 = Car(num_plate='bf6 h8w', ownerbr=testuser)
    db.session.add(testcar2)
    db.session.commit()
    testcar3 = Car(num_plate='bf5 h8w', ownerbr=testuser)
    db.session.add(testcar3)
    db.session.commit()

    print(testcar.ownerbr.first_name)
    print(testuser.cars[1].num_plate)

    testitem = Car.query.filter_by(owner_id=1).order_by(Car.id.desc()).all()
    # print(testitem)

    car_to_change = Car.query.filter_by(id=1).first()
    car_to_change.num_plate = "new number plate"
    db.session.commit()

    car_to_delete = Car.query.filter_by(id=2).first()
    db.session.delete(car_to_delete)
    db.session.commit()

    var1 = bcrypt.generate_password_hash('bf6 h8w')
    print(bcrypt.check_password_hash(b'$2b$12$UEokINQX20q3GrrzSa4OJOb/Mc4wqv2rvX4.b/.t2fbQ6aCF7ldRi', 'bf6 h8w'))