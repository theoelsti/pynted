class VintedUser:
    """A user on Vinted platform."""

    def __init__(self, config: dict) -> None:
        """Initialize a VintedUser from a config dictionary.

        Args:
            config (dict): A dictionary with user data. Expected keys are
                "id", "about", "login", "real_name", "email", "photo", "config",
                "given_item_count", "taken_item_count", "feedback_reputation",
                "positive_feedback_count", "neutral_feedback_count",
                "negative_feedback_count", "feedback_count", "bundle_discount",
                "country_iso_code", and "verification".
        """
        self.user_id = config.get("id")
        self.bio = config.get("about")
        self.personnal_infos = {
            "username": config.get("login"),
            "name": config.get("real_name"),
            "email": config.get("email"),
            "profile_picture": config.get("photo", {}).get("url"),
            "color": config.get("config", {}).get("photo", {}).get("dominant_color"),
        }
        self.stats = {
            "given_item_count": config.get("given_item_count"),
            "taken_item_count": config.get("taken_item_count"),
            "feedback_reputation": config.get("feedback_reputation"),
            "positive_feedback_count": config.get("positive_feedback_count"),
            "neutral_feedback_count": config.get("neutral_feedback_count"),
            "negative_feedback_count": config.get("negative_feedback_count"),
            "feedback_count": config.get("feedback_count"),
        }
        self.bundle_discount = config.get("bundle_discount")
        self.country_iso_code = config.get("country_iso_code")
        self.verification = {}
        for key in ["email", "phone", "facebook", "google"]:
            self.verification[key] = bool(
                config.get("verification", {}).get(key, {}).get("valid")
            )
