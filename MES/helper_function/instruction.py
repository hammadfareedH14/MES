
from models.part import PartModel

def arrayformat(parts):
    parts_data = []
    for part in parts:
        # Ensure 'value' and 'image_url' exist in each part
        if 'value' in part and 'image_url' in part:
            # Append the part information as a dictionary to parts_data
            parts_data.append({
                "part_id": part['value'],  # Treating 'value' as the part ID
                "image_url": part['image_url']
            })
        else:
            raise ValueError("Invalid part format. Each part must have 'value' and 'image_url'.")
    return parts_data 


def get_part(part_id):
    # Retrieve the part using the provided part_id
    part = PartModel.query.filter_by(id=part_id).first()

    # If part does not exist, return None
    if not part:
        return None

    # Create the detailed part structure
    parts_data = {
        "part": {
            "number": part.number,
            "description": part.description,
            "_id": part.id,
            "category_id": part.category_id,
            "route_id": part.route_id,
        },
        "categories": {
            "name": part.categories.name,
            "type": part.categories._type.value,  # Assuming _type is an Enum in your Category model
            "_id": part.categories.id,
        },
        "route": {
            "name": part.routes.name,
            "description": part.routes.description,
            "_id": part.routes.id,
        }
    }

    return parts_data
