from marshmallow import Schema, fields, validate, pre_load, post_load


class PlaceSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(max=256))
    imgs = fields.List(fields.String())
    description_short = fields.String()
    description_long = fields.String()
    lng = fields.Float(
        required=True,
        validate=validate.Range(min_inclusive=-180, max_inclusive=180)
    )
    lat = fields.Float(
        required=True,
        validate=validate.Range(min_inclusive=-90, max_inclusive=90)
    )

    class Meta:
        fields = [
            'title',
            'imgs',
            'description_short',
            'description_long',
            'lng',
            'lat'
        ]

    @pre_load
    def process_coords(self, in_data, **kwargs):
        coordinates = in_data.pop('coordinates')
        in_data['lat'] = coordinates['lat']
        in_data['lng'] = coordinates['lng']
        return in_data

    @post_load
    def round_coords(self, in_data, **kwargs):
        in_data['lat'] = round(in_data['lat'], 5)
        in_data['lng'] = round(in_data['lng'], 5)
        return in_data
