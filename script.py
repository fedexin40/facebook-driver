import csv
import json
from python_graphql_client import GraphqlClient
from queries import query_offset, query

# Instantiate the client with an endpoint.
client = GraphqlClient(endpoint="https://api.proyecto705.com/graphql/")

first = 100
variables = {"first": first}
# Synchronous request
result = client.execute(query=query, variables=variables)

link_template_string = "https://proyecto705.com/{collection}/{product_slug}"
# Write header
with open('feed.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = [
        'id', 'title', 'description', 'availability', 'condition',
        'price', 'link', 'image_link', 'brand', 'google_product_category',
        'plating_material', 'additional_image_link', 'internal_label']
    writer.writerow(field)
    while True:
        # Get products from data
        products = result['data']['products']['edges']
        if not products:
            break
        # Get cursor from last product fetched
        cursor = products[-1]['cursor']
        variables = {"first": first, "cursor": cursor}
        for product in products:
            product = product['node']
            collections = product['collections']
            category = product['category']['slug']
            id = product['slug']
            title = product['name']
            description = product['description']
            description = str(
                json.loads(description)['blocks'][1]['data']['text'] if description
                else ''
            )
            description = description.replace('&nbsp;', '')
            availability = 'in stock' if product['isAvailable'] else 'out of stock'
            # I only sell new products :)
            condition = 'new'
            price = ' '.join([
                str(product['pricing']['priceRange']['stop']['net']['amount']),
                str(product['pricing']['priceRange']['stop']['net']['currency'])
            ])
            # It is possible to have more than one image, then I am taking the
            # first one
            image_link = product['media'][0]['url']
            additional_image_link = (x['url'] for x in product['media'][1:])
            additional_image_link = ','.join(additional_image_link)
            url = "https://proyecto705.com/Colecciones/{collection}/{product_slug}".format(
                collection=collections[0]['slug'], product_slug=product['slug']
            )
            brand = 'Proyecto 705'
            internal_label = list(x['slug']for x in collections)
            internal_label.append(category)
            writer.writerow(
                [id, title, description, availability, condition,
                 price, url, image_link, brand, '194', 'Gold',
                 additional_image_link, internal_label])
        # Lets get the next products
        variables = {"first": first, "cursor": cursor}
        result = client.execute(query=query_offset, variables=variables)
