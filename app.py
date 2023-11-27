from flask import Flask, request, jsonify
import math
from static.celestial_bodies import celestial_bodies

app = Flask(__name__)


def calculate_space_velocities(mass, radius):
    G = 6.67430e-11  # stała grawitacyjna
    v1 = math.sqrt(G * mass / radius)  # Pierwsza prędkość kosmiczna
    v2 = math.sqrt(2) * v1            # Druga prędkość kosmiczna
    return v1, v2


@app.route('/space_velocities', methods=['POST'])
def space_velocities():
    """
    Calculates the first and second cosmic velocities for a given celestial body.

    Accepts a JSON with one of two sets of data:
    1. Name of the celestial body (body_name) - uses predefined values for mass and radius.
    2. Mass (mass) and radius (radius) of the celestial body - calculates velocities based on these data.

    Example request with the name of a celestial body:
    {
        "body_name": "Mars"
    }

    Example request with mass and radius:
    {
        "body_name": "some_body_name", (optional)
        "mass": 6.0e24,
        "radius": 6.4e6
    }

    Returns:
    A JSON object containing:
    - 'body_name': The name of the celestial body (if provided or null).
    - 'first_velocity': Calculated first cosmic velocity in meters per second.
    - 'second_velocity': Calculated second cosmic velocity in meters per second.

    In case of invalid input, returns a JSON object with an 'error' key and a 400 status code.
    """
    data = request.json
    body_name = data.get('body_name')
    mass = data.get('mass')
    radius = data.get('radius')

    if mass is None and radius is None:
        if body_name and body_name in celestial_bodies:
            body = celestial_bodies[body_name]
            mass, radius = body['mass'], body['radius']
        else:
            return jsonify({"error": "Either predefined celestial body name or custom mass and radius must be provided"}), 400
    elif mass is not None and radius is not None:
        if mass <= 0 or radius <= 0:
            return jsonify({"error": "Mass and radius must be positive numbers"}), 400
        # Check for unrealistic values
        if mass > 1e32 or radius > 1e9:
            return jsonify({"error": "Mass or radius values are unrealistically large"}), 400
    else:
        return jsonify({"error": "Incomplete data: both mass and radius are required for custom calculations"}), 400

    v1, v2 = calculate_space_velocities(mass, radius)

    return jsonify({"body_name": body_name, "first_velocity": v1, "second_velocity": v2})


if __name__ == '__main__':
    app.run(debug=True)
