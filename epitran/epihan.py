import os.path

import pkg_resources
import regex as re

from epitran.ligaturize import ligaturize

from . import cedict, download, rules


class MissingData(Exception):
    pass


class Epihan:
    punc = [
        ("\uff0c", ","),
        ("\uff01", "!"),
        ("\uff1f", "?"),
        ("\uff1b", ";"),
        ("\uff1a", ":"),
        ("\uff08", "("),
        ("\uff09", ")"),
        ("\uff3b", "["),
        ("\uff3d", "]"),
        ("\u3010", "["),
        ("\u3011", "]"),
    ]

    def __init__(
        self,
        ligatures=False,
        cedict_file=None,
        rules_file="pinyin-to-ipa.txt",
        tones=False,
    ):
        """Construct epitran object for Chinese

        Args:
            ligatures (bool): if True, use ligatures instead of standard IPA
            cedict_file (str): path to CC-CEDict dictionary file
            rules_file (str): name of file with rules for converting pinyin to
                              IPA
            tones (bool): if True, output tones as Chao tone numbers; overrides
                          `rules_file`
        """
        # If no cedict_file is specified, raise and error
        if not cedict_file:
            if download.cedict_exists():
                cedict_file = download.get_cedict_file()
            else:
                raise MissingData('Download CC-CEDICT with "epitran.download.cedict()')
        if tones:
            rules_file = os.path.join("data", "rules", "pinyin-to-ipa-tones.txt")
        else:
            rules_file = os.path.join("data", "rules", rules_file)
        rules_file = pkg_resources.resource_filename(__name__, rules_file)
        self.cedict = cedict.CEDictTrie(cedict_file)
        self.rules = rules.Rules([rules_file])
        self.regexp = re.compile(r"\p{Han}")

    def normalize_punc(self, text):
        """Normalize punctutation in a string

        Args:
            text (unicode): an orthographic string

        Return:
            unicode: an orthographic string with punctation normalized to
                     Western equivalents
        """
        for a, b in self.punc:
            text = text.replace(a, b)
        return text

    def transliterate(self, text, normpunc=False, ligatures=False):
        """Transliterates/transcribes a word into IPA

        Args:
            word (str): word to transcribe; Unicode string
            normpunc (bool): normalize punctuation
            ligatures (bool): use precomposed ligatures instead of standard IPA

        Returns:
            str: Unicode IPA string
        """
        tokens = self.cedict.tokenize(text)
        ipa_tokens = []
        for token in tokens:
            if token in self.cedict.hanzi:
                (pinyin, _) = self.cedict.hanzi[token]
                pinyin = "".join(pinyin).lower()
                ipa = self.rules.apply(pinyin)
                ipa_tokens.append(ipa.replace(",", ""))
            else:
                if normpunc:
                    token = self.normalize_punc(token)
                ipa_tokens.append(token)
        ipa_tokens = map(ligaturize, ipa_tokens) if ligatures else ipa_tokens
        return "".join(ipa_tokens)

    def strict_trans(self, text, normpunc=False, ligatures=False):
        return self.transliterate(text, normpunc, ligatures)


class EpihanTraditional(Epihan):
    def __init__(
        self,
        ligatures=False,
        cedict_file=None,
        tones=False,
        rules_file="pinyin-to-ipa.txt",
    ):
        """Construct epitran object for Traditional Chinese

        Args:
            ligatures (bool): if True, use ligatures instead of standard IPA
            cedict_file (str): path to CC-CEDict dictionary file
            rules_file (str): name of file with rules for converting pinyin to
                              IPA
        """
        if not cedict_file:
            if download.cedict_exists():
                cedict_file = download.get_cedict_file()
            else:
                raise MissingData('Download CC-CEDICT with "epitran.download.cedict().')
        if tones:
            rules_file = os.path.join("data", "rules", "pinyin-to-ipa-tones.txt")
        else:
            rules_file = os.path.join("data", "rules", rules_file)
        rules_file = pkg_resources.resource_filename(__name__, rules_file)
        self.cedict = cedict.CEDictTrie(cedict_file, traditional=True)
        self.rules = rules.Rules([rules_file])
        self.regexp = re.compile(r"\p{Han}")
