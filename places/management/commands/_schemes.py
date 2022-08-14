from marshmallow import Schema, fields, validate, validates, ValidationError


class PlaceSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(max=256))
    imgs = fields.List(fields.String())
    description_short = fields.String()
    description_long = fields.String()
    coordinates = fields.Dict(keys=fields.String(), values=fields.Float())

    @validates("coordinates")
    def validate_coordinates(self, dct):
        if 'lat' not in dct or 'lng' not in dct:
            raise ValidationError("Coordinates are missed or incorrect")
        if not -90 <= dct['lat'] <= 90 or not -180 <= dct['lng'] <= 180:
            raise ValidationError("Wrong latitude and/or longitude value")