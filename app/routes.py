from flask import abort, Flask, make_response, redirect, request, url_for

from app import db
from app.models import CarsModel


def init_routes(app: Flask):
    @app.route('/')
    def app_root():
        return redirect(url_for('api_root'))

    @app.route('/api')
    def api_root():
        return {'message': 'This is the API root url.', 'status': 200}

    @app.route('/api/cars', methods=('GET', 'POST'))
    def handle_cars():
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                if not data.get('name') or not data.get('model') or not data.get('doors'):
                    abort(make_response(
                        {'message': 'Mandatory fields are missing: [name, model, doors].', 'status': 400},
                        400
                    ))
                new_car = CarsModel(
                    name=data['name'],
                    model=data['model'],
                    doors=data['doors']
                )
                db.session.add(new_car)
                db.session.commit()
                return {'message': f'Car {new_car.name} has been created successfully.', 'status': 201}, 201
            else:
                abort(make_response({'message': 'Unsupported media type.', 'status': 415}, 415))
        elif request.method == 'GET':
            cars = CarsModel.query.all()
            cars_list = [
                {
                    'name': car.name,
                    'model': car.model,
                    'doors': car.doors
                }
                for car in cars
            ]
            return {'cars': cars_list, 'total': len(cars_list), 'status': 200}

    @app.route('/api/cars/<car_id>', methods=('GET', 'PUT', 'DELETE'))
    def handle_car(car_id):
        car = CarsModel.query.get_or_404(car_id)

        if request.method == 'GET':
            return {
                'car': {
                    'name': car.name,
                    'model': car.model,
                    'doors': car.doors
                },
                'status': 200
            }
        elif request.method == 'PUT':
            if request.is_json:
                data = request.get_json()
                if not data.get('name') or not data.get('model') or not data.get('doors'):
                    abort(make_response(
                        {'message': 'Mandatory fields are missing: [name, model, doors].', 'status': 400},
                        400
                    ))
                car.name = data['name']
                car.model = data['model']
                car.doors = data['doors']
                db.session.add(car)
                db.session.commit()
                return {'message': f'Car {car.name} successfully updated.', 'status': 200}
            else:
                abort(make_response({'message': 'Unsupported media type.', 'status': 415}, 415))
        elif request.method == 'DELETE':
            db.session.delete(car)
            db.session.commit()
            return {'message': f'Car {car.name} successfully deleted.', 'status': 200}
