from rest_framework.response import Response

def return_products(n):
    dm = n['id']
    return {
            "id": dm, 
            "name": n['name'], 
            "description": n['description'],
            # "image": n['image'],
            "image": f'http://drugstoc.odoo.com/web/image/product.product/{dm}/image',
            "price": n['list_price'],
            "composition": n['x_studio_field_5Gttm'],
            "manufacturer": n['x_studio_field_xH9Vy'],
            "quantity": int(n['qty_available']),
            "category": n['categ_id'][1],
            "create_date": n['create_date']
        } 

def return_user(n):
    if n['email'] is not False:
            return {
                "erp_id": n['id'], 
                "name": n['name'], 
                "password": "123456",
                "phone_no": n['phone'] or n['mobile'],
                "email": n['email'],
                "category": n['x_studio_field_vM2kZ']
            } 
    else:
            return {
                "erp_id": n['id'], 
                "name": n['name'], 
                "password": "123456",
                "phone_no": n['phone'] or n['mobile'],
                "email": n['name'],
                "category": n['x_studio_field_vM2kZ']
            } 

def return_categories(n):
    return {
        "id": n['id'],
        "name": n['name'],
        "total_products": n['product_count'],
         "create_date": n['create_date']
    }

def return_manufacturer(n):
    if n['x_studio_field_xH9Vy'] is not False:
        return {
            "name": n['x_studio_field_xH9Vy'],
        }
    else:
        return {
            "name": "Others"
        }

def return_orders(n):
    return {
        "id": n['id'],
        "name": n['name'],
        "status": n["state"],
        "author": n["user_id"][1],
        "customer": n['partner_id'][1],
        "total_cost": n["amount_untaxed"],
        "vat": n['amount_tax'],
        "total_product": (len(n["order_line"])),
        "total_amount": n['amount_total'],
        "created_date": n["date_order"],
        # "payment_terms": n['payment_term_id'][1]
    }

def return_order_details(n):
    dm = n["product_id"][0]
    return {
        "id": dm,
        "name": n['name'],
        "status": n["state"],
        "salesman": n["salesman_id"][1],
        "customer": n["order_partner_id"][1],
        "total_cost": n["price_subtotal"],
        "total_amount": n['price_total'],
        "price": n['price_unit'],
        "image": f'https://drugstoc.odoo.com/web/image/product.product/{dm}/image',
        "quantity": n['product_uom_qty'],
        "created_date": n["create_date"],
    }

def unique(list1):
    unique_list = []
    for x in list1:
        if x['x_studio_field_xH9Vy'] not in unique_list:
            unique_list.append(x)
    return unique_list

def return_response(request, data, total, offset):
    page = request.query_params.get('page')
    uro = request.build_absolute_uri('')
    page_number = 1 if page == None else int(page)
    next_page = f'{uro}?page={page_number + 1}' if total > offset + 50 else None
    prev_page = None if page == None or total < offset else uro if int(page) <= 2 else f'{uro}?page={page_number - 1}'
    return Response({"count": total,  "next": next_page, "previous": prev_page, "results": data}, status=200)