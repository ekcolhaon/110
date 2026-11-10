from flask import Flask, jsonify, request

app = Flask(__name__)

students_cohort_71 = ["Cameron", "Angelina", "Noah", "Isaac", "Andy"]

course_information = {
    "course_name": "APIs with Python and Flask",
    "sessions": 4,
    "description": "Introduction to APIs and endpoints using Python and Flask"
}

products = [
    {"_id": 1, "title": "Laptop", "price": 999.99, "category": "Electronics"},
    {"_id": 2, "title": "Headphones", "price": 79.99, "category": "Electronics"},
    {"_id": 3, "title": "Keyboard", "price": 49.99, "category": "Accessories"}
]

coupons = [
    {"_id": 1, "code": "WELCOME10", "discount": 10},
    {"_id": 2, "code": "SPOOKY25", "discount": 25},
    {"_id": 3, "code": "VIP50", "discount": 50}
]


@app.get("/")
def home():
    return jsonify({"message": "Welcome to Cohort 71 Online Store API"})


@app.get("/say-hi")
def function_to_say_hi():
    return jsonify("Hello cohort 71")


@app.get("/say-boo")
def say_boo():
    return jsonify("Boo")


@app.get("/students-71")
def get_students_71():
    return jsonify({"students": students_cohort_71})


@app.get("/course-information")
def get_course_information():
    return jsonify({"course_information": course_information})


@app.get("/api/products")
def get_products():
    return jsonify({"products": products})


@app.get("/api/products/<int:product_id>")
def get_product_by_id(product_id):
    for product in products:
        if product["_id"] == product_id:
            return jsonify({
                "success": True,
                "message": "Product retrieved successfully",
                "data": product
            }), 200

    return jsonify({
        "success": False,
        "message": "Product not found"
    }), 404


@app.post("/api/products")
def create_product():
    new_product = request.get_json(silent=True)

    if not isinstance(new_product, dict):
        return jsonify({"message": "Invalid product data"}), 400

    if "title" not in new_product or "price" not in new_product:
        return jsonify({"message": "Title and price are required"}), 400

    if (not isinstance(new_product["title"], str)
            or not new_product["title"].strip()
            or isinstance(new_product["price"], bool)
            or not isinstance(new_product["price"], (int, float))
            or not 0 <= new_product["price"] < float("inf")):
        return jsonify({"message": "Invalid title or price"}), 400

    new_product["_id"] = max(
        (product["_id"] for product in products),
        default=0
    ) + 1

    products.append(new_product)

    return jsonify({
        "success": True,
        "message": "Product created successfully",
        "data": new_product
    }), 201


@app.delete("/api/products/<int:product_id>")
def delete_product(product_id):
    for product in products:
        if product["_id"] == product_id:
            products.remove(product)

            return jsonify({
                "success": True,
                "message": "Product deleted successfully",
                "deleted_product": product
            }), 200

    return jsonify({
        "success": False,
        "message": "Product not found"
    }), 404


@app.get("/api/coupons")
def get_coupons():
    return jsonify({"coupons": coupons})


@app.get("/api/coupons/count")
def get_coupon_count():
    return jsonify({"count": len(coupons)})


@app.get("/api/coupons/<int:coupon_id>")
def get_coupon(coupon_id):
    for coupon in coupons:
        if coupon["_id"] == coupon_id:
            return jsonify({
                "success": True,
                "data": coupon
            }), 200

    return jsonify({
        "success": False,
        "message": "Coupon not found"
    }), 404


@app.post("/api/coupons")
def add_coupon():
    new_coupon = request.get_json(silent=True)

    if not isinstance(new_coupon, dict):
        return jsonify({"message": "Invalid coupon data"}), 400

    code = new_coupon.get("code")
    discount = new_coupon.get("discount")

    if (not isinstance(code, str)
            or not code.strip()
            or isinstance(discount, bool)
            or not isinstance(discount, (int, float))
            or not 0 <= discount <= 100):
        return jsonify({"message": "Invalid code or discount"}), 400

    if any(coupon["code"] == code for coupon in coupons):
        return jsonify({"message": "Coupon already exists"}), 409

    new_coupon["_id"] = max(
        (coupon["_id"] for coupon in coupons),
        default=0
    ) + 1

    coupons.append(new_coupon)

    return jsonify({
        "success": True,
        "message": "Coupon added successfully",
        "data": new_coupon
    }), 201


@app.delete("/api/coupons/<int:coupon_id>")
def delete_coupon(coupon_id):
    for coupon in coupons:
        if coupon["_id"] == coupon_id:
            coupons.remove(coupon)

            return jsonify({
                "success": True,
                "message": "Coupon deleted successfully"
            }), 200

    return jsonify({
        "success": False,
        "message": "Coupon not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
