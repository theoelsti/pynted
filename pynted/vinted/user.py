class VintedUser():
    def __init__(self, config: dict) -> None:
        self.id = config["id"]
        self.bio = config["about"]
        self.personnal_infos = {
            "username": config["login"],
            "name": config["real_name"],
            "email": config["email"],
            "profile_picture": config["photo"]["url"],
            "color": config["config"]["photo"]["dominant_color"]
        }
        self.transactions = {
            "sales": config["given_item_count"],
            "purchases": config["taken_item_count"]
        }
        self.feedbacks = {
            "ratio": config["feedback_reputation"],
            "positive": config["positive_feedback_count"],
            "neutral": config["neutral_feedback_count"],
            "negative": config["negative_feedback_count"],
            "count": config["feedback_count"]

        }
        self.discounts = {
            config["bundle_discount"]["discounts"]
        }
        self.country = config["country_iso_code"]
        self.verification = {
            "email": True if config["verification"]["email"]["valid"] else False,
            "phone": True if config["verification"]["phone"]["valid"] else False,
            "facebook": True if config["verification"]["facebook"]["valid"] else False,
            "google": True if config["verification"]["google"]["valid"] else False,
        }
