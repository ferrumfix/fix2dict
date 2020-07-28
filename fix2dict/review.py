class RepositoryReview:
    def __init__(self, repo):
        self.abbreviations = len(repo["abbreviations"])
        self.datatypes = len(repo["datatypes"])
        self.components = len(repo["components"])
        self.fields = len(repo["fields"])
        self.messages = len(repo["messages"])
        self.messages_breakdown = {}
        for s in repo["sections"]:
            self.messages_breakdown[s] = {}
            for (c, c_val) in repo["categories"].items():
                if c_val["section"] == s:
                    self.messages_breakdown[s][c] = 0
                    for m_val in repo["messages"].values():
                        if m_val["section"] == s and m_val["category"] == c:
                            self.messages_breakdown[s][c] += 1

    def __str__(self):
        s = """FIX2dict-flavoured FIX Repository data
+ Abbreviations: {:>4}
+ Datatypes:     {:>4}
+ Components:    {:>4}
+ Fields:        {:>4}
+ Messages:      {:>4}
  By section and category:""".format(
            self.abbreviations,
            self.datatypes,
            self.components,
            self.fields,
            self.messages,
        )
        for (section, by_section) in self.messages_breakdown.items():
            s += "\n  + Sect. '{}': {}".format(
                section, sum([n for n in by_section.values()])
            )
            for (category, count) in by_section.items():
                s += "\n    + Cat. '{}': {}".format(category, count)
        return s

    def to_dict(self):
        return {
            "abbreviations": self.abbreviations,
            "datatypes": self.datatypes,
            "components": self.components,
            "fields": self.fields,
            "messages": self.messages,
            "messagesBreakdown": self.messages_breakdown,
        }
