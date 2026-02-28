from functools import cache

from nd_utility.data.kind.dic.dic import Dic


class Schema:
    @cache
    def get_schema_dic(self) -> Dic:
        return Dic \
                (
                {
                    "memory": {
                        "explicit": {
                            "long_term": {
                                "episodic": {},
                                "semantic": {}
                            },
                            # short term is also working memory
                            "working": {}
                        }
                    },
                    "implicit": {
                        "skills": {},
                        "repetition_priming": {
                            "sequence_to_sequence_models": {}
                        }
                    }
                }
        )

    def draw(self):
        self.get_schema_dic().draw()


if __name__ == "__main__":
    schema = Schema().draw()
