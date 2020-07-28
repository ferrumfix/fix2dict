class FixVersion:
    def __init__(self, val: str, ep=None):
        if "_EP" in val:
            val, ep = tuple(val.split("_EP"))
        if "SP" in val:
            val, sp = tuple(val.split("SP"))
        else:
            sp = "0"
        protocol, major, minor = tuple(val.split("."))
        protocol = protocol.lower()
        self.data = {
            "fix": protocol,
            "major": major,
            "minor": minor,
            "sp": sp,
        }
        if ep:
            self.data["ep"] = ep

    @classmethod
    def create_from_xml_attrs(cls, attrs, keyword):
        ep = keyword + "EP"
        if keyword in attrs and ep in attrs and attrs[ep] != "-1":
            return cls(attrs[keyword], attrs[ep])
        elif keyword in attrs:
            return cls(attrs[keyword])
        else:
            return None
