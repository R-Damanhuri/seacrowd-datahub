import json
from pathlib import Path
from typing import Dict, List, Tuple

import datasets
import pandas as pd

from seacrowd.utils import schemas
from seacrowd.utils.configs import SEACrowdConfig
from seacrowd.utils.constants import Tasks, Licenses

_CITATION = """\
@article{mahadi2023indonesian,
    author    = {Made Raharja Surya Mahadi and Nugraha Priya Utama},
    title     = {Indonesian Text-to-Image Synthesis with Sentence-BERT and FastGAN},
    journal   = {arXiv preprint arXiv:2303.14517},
    year      = {2023},
    url       = {https://arxiv.org/abs/2303.14517},
}
"""

_DATASETNAME = "cub_bahasa"
_DESCRIPTION = """\
Semi-translated dataset of CUB-200-2011 into Indonesian. This dataset contains thousands
of image-text annotation pairs of 200 subcategories belonging to birds. The natural
language descriptions are collected through the Amazon Mechanical Turk (AMT) platform and
are required at least 10 words, without any information on subcategories and actions.
"""

_LOCAL=False
_LANGUAGES = ["ind"]  # We follow ISO639-3 language code (https://iso639-3.sil.org/code_tables/639/data)

_HOMEPAGE = "https://github.com/share424/Indonesian-Text-to-Image-synthesis-with-Sentence-BERT-and-FastGAN"
_LICENSE = Licenses.UNKNOWN.value
_URLS = {
    "text": "https://raw.githubusercontent.com/share424/Indonesian-Text-to-Image-synthesis-with-Sentence-BERT-and-FastGAN/master/dataset/indo_cub_200_2011_captions.json",
    "image": "https://data.caltech.edu/records/65de6-vp158/files/CUB_200_2011.tgz"
}

_SUPPORTED_TASKS = [Tasks.IMAGE_CAPTIONING]
_SOURCE_VERSION = "1.0.0"
_SEACROWD_VERSION = "2024.06.20"


class CubBahasaDataset(datasets.GeneratorBasedBuilder):
    """CUB-200-2011 image-text dataset in Indonesian language for bird domain."""

    SOURCE_VERSION = datasets.Version(_SOURCE_VERSION)
    SEACROWD_VERSION = datasets.Version(_SEACROWD_VERSION)

    SEACROWD_SCHEMA_NAME = "imtext"
    IMAGE_CLASS = {
        1: '001.Black_footed_Albatross',
        2: '002.Laysan_Albatross',
        3: '003.Sooty_Albatross',
        4: '004.Groove_billed_Ani',
        5: '005.Crested_Auklet',
        6: '006.Least_Auklet',
        7: '007.Parakeet_Auklet',
        8: '008.Rhinoceros_Auklet',
        9: '009.Brewer_Blackbird',
        10: '010.Red_winged_Blackbird',
        11: '011.Rusty_Blackbird',
        12: '012.Yellow_headed_Blackbird',
        13: '013.Bobolink',
        14: '014.Indigo_Bunting',
        15: '015.Lazuli_Bunting',
        16: '016.Painted_Bunting',
        17: '017.Cardinal',
        18: '018.Spotted_Catbird',
        19: '019.Gray_Catbird',
        20: '020.Yellow_breasted_Chat',
        21: '021.Eastern_Towhee',
        22: '022.Chuck_will_Widow',
        23: '023.Brandt_Cormorant',
        24: '024.Red_faced_Cormorant',
        25: '025.Pelagic_Cormorant',
        26: '026.Bronzed_Cowbird',
        27: '027.Shiny_Cowbird',
        28: '028.Brown_Creeper',
        29: '029.American_Crow',
        30: '030.Fish_Crow',
        31: '031.Black_billed_Cuckoo',
        32: '032.Mangrove_Cuckoo',
        33: '033.Yellow_billed_Cuckoo',
        34: '034.Gray_crowned_Rosy_Finch',
        35: '035.Purple_Finch',
        36: '036.Northern_Flicker',
        37: '037.Acadian_Flycatcher',
        38: '038.Great_Crested_Flycatcher',
        39: '039.Least_Flycatcher',
        40: '040.Olive_sided_Flycatcher',
        41: '041.Scissor_tailed_Flycatcher',
        42: '042.Vermilion_Flycatcher',
        43: '043.Yellow_bellied_Flycatcher',
        44: '044.Frigatebird',
        45: '045.Northern_Fulmar',
        46: '046.Gadwall',
        47: '047.American_Goldfinch',
        48: '048.European_Goldfinch',
        49: '049.Boat_tailed_Grackle',
        50: '050.Eared_Grebe',
        51: '051.Horned_Grebe',
        52: '052.Pied_billed_Grebe',
        53: '053.Western_Grebe',
        54: '054.Blue_Grosbeak',
        55: '055.Evening_Grosbeak',
        56: '056.Pine_Grosbeak',
        57: '057.Rose_breasted_Grosbeak',
        58: '058.Pigeon_Guillemot',
        59: '059.California_Gull',
        60: '060.Glaucous_winged_Gull',
        61: '061.Heermann_Gull',
        62: '062.Herring_Gull',
        63: '063.Ivory_Gull',
        64: '064.Ring_billed_Gull',
        65: '065.Slaty_backed_Gull',
        66: '066.Western_Gull',
        67: '067.Anna_Hummingbird',
        68: '068.Ruby_throated_Hummingbird',
        69: '069.Rufous_Hummingbird',
        70: '070.Green_Violetear',
        71: '071.Long_tailed_Jaeger',
        72: '072.Pomarine_Jaeger',
        73: '073.Blue_Jay',
        74: '074.Florida_Jay',
        75: '075.Green_Jay',
        76: '076.Dark_eyed_Junco',
        77: '077.Tropical_Kingbird',
        78: '078.Gray_Kingbird',
        79: '079.Belted_Kingfisher',
        80: '080.Green_Kingfisher',
        81: '081.Pied_Kingfisher',
        82: '082.Ringed_Kingfisher',
        83: '083.White_breasted_Kingfisher',
        84: '084.Red_legged_Kittiwake',
        85: '085.Horned_Lark',
        86: '086.Pacific_Loon',
        87: '087.Mallard',
        88: '088.Western_Meadowlark',
        89: '089.Hooded_Merganser',
        90: '090.Red_breasted_Merganser',
        91: '091.Mockingbird',
        92: '092.Nighthawk',
        93: '093.Clark_Nutcracker',
        94: '094.White_breasted_Nuthatch',
        95: '095.Baltimore_Oriole',
        96: '096.Hooded_Oriole',
        97: '097.Orchard_Oriole',
        98: '098.Scott_Oriole',
        99: '099.Ovenbird',
        100: '100.Brown_Pelican',
        101: '101.White_Pelican',
        102: '102.Western_Wood_Pewee',
        103: '103.Sayornis',
        104: '104.American_Pipit',
        105: '105.Whip_poor_Will',
        106: '106.Horned_Puffin',
        107: '107.Common_Raven',
        108: '108.White_necked_Raven',
        109: '109.American_Redstart',
        110: '110.Geococcyx',
        111: '111.Loggerhead_Shrike',
        112: '112.Great_Grey_Shrike',
        113: '113.Baird_Sparrow',
        114: '114.Black_throated_Sparrow',
        115: '115.Brewer_Sparrow',
        116: '116.Chipping_Sparrow',
        117: '117.Clay_colored_Sparrow',
        118: '118.House_Sparrow',
        119: '119.Field_Sparrow',
        120: '120.Fox_Sparrow',
        121: '121.Grasshopper_Sparrow',
        122: '122.Harris_Sparrow',
        123: '123.Henslow_Sparrow',
        124: '124.Le_Conte_Sparrow',
        125: '125.Lincoln_Sparrow',
        126: '126.Nelson_Sharp_tailed_Sparrow',
        127: '127.Savannah_Sparrow',
        128: '128.Seaside_Sparrow',
        129: '129.Song_Sparrow',
        130: '130.Tree_Sparrow',
        131: '131.Vesper_Sparrow',
        132: '132.White_crowned_Sparrow',
        133: '133.White_throated_Sparrow',
        134: '134.Cape_Glossy_Starling',
        135: '135.Bank_Swallow',
        136: '136.Barn_Swallow',
        137: '137.Cliff_Swallow',
        138: '138.Tree_Swallow',
        139: '139.Scarlet_Tanager',
        140: '140.Summer_Tanager',
        141: '141.Artic_Tern',
        142: '142.Black_Tern',
        143: '143.Caspian_Tern',
        144: '144.Common_Tern',
        145: '145.Elegant_Tern',
        146: '146.Forsters_Tern',
        147: '147.Least_Tern',
        148: '148.Green_tailed_Towhee',
        149: '149.Brown_Thrasher',
        150: '150.Sage_Thrasher',
        151: '151.Black_capped_Vireo',
        152: '152.Blue_headed_Vireo',
        153: '153.Philadelphia_Vireo',
        154: '154.Red_eyed_Vireo',
        155: '155.Warbling_Vireo',
        156: '156.White_eyed_Vireo',
        157: '157.Yellow_throated_Vireo',
        158: '158.Bay_breasted_Warbler',
        159: '159.Black_and_white_Warbler',
        160: '160.Black_throated_Blue_Warbler',
        161: '161.Blue_winged_Warbler',
        162: '162.Canada_Warbler',
        163: '163.Cape_May_Warbler',
        164: '164.Cerulean_Warbler',
        165: '165.Chestnut_sided_Warbler',
        166: '166.Golden_winged_Warbler',
        167: '167.Hooded_Warbler',
        168: '168.Kentucky_Warbler',
        169: '169.Magnolia_Warbler',
        170: '170.Mourning_Warbler',
        171: '171.Myrtle_Warbler',
        172: '172.Nashville_Warbler',
        173: '173.Orange_crowned_Warbler',
        174: '174.Palm_Warbler',
        175: '175.Pine_Warbler',
        176: '176.Prairie_Warbler',
        177: '177.Prothonotary_Warbler',
        178: '178.Swainson_Warbler',
        179: '179.Tennessee_Warbler',
        180: '180.Wilson_Warbler',
        181: '181.Worm_eating_Warbler',
        182: '182.Yellow_Warbler',
        183: '183.Northern_Waterthrush',
        184: '184.Louisiana_Waterthrush',
        185: '185.Bohemian_Waxwing',
        186: '186.Cedar_Waxwing',
        187: '187.American_Three_toed_Woodpecker',
        188: '188.Pileated_Woodpecker',
        189: '189.Red_bellied_Woodpecker',
        190: '190.Red_cockaded_Woodpecker',
        191: '191.Red_headed_Woodpecker',
        192: '192.Downy_Woodpecker',
        193: '193.Bewick_Wren',
        194: '194.Cactus_Wren',
        195: '195.Carolina_Wren',
        196: '196.House_Wren',
        197: '197.Marsh_Wren',
        198: '198.Rock_Wren',
        199: '199.Winter_Wren',
        200: '200.Common_Yellowthroat'
    }

    BUILDER_CONFIGS = [
        SEACrowdConfig(
            name=f"{_DATASETNAME}_source",
            version=SOURCE_VERSION,
            description=f"{_DATASETNAME} source schema",
            schema="source",
            subset_id=f"{_DATASETNAME}",
        ),
        SEACrowdConfig(
            name=f"{_DATASETNAME}_seacrowd_{SEACROWD_SCHEMA_NAME}",
            version=SEACROWD_VERSION,
            description=f"{_DATASETNAME} SEACrowd schema",
            schema=f"seacrowd_{SEACROWD_SCHEMA_NAME}",
            subset_id=f"{_DATASETNAME}",
        ),
    ]

    DEFAULT_CONFIG_NAME = f"{_DATASETNAME}_source"

    def _info(self) -> datasets.DatasetInfo:
        if self.config.schema == "source":
            features = datasets.Features(
                {
                    "image_id": datasets.Value("int64"),
                    "class_id": datasets.Value("int64"),
                    "image_path": datasets.Value("string"),
                    "class_name": datasets.Value("string"),
                    "captions": [
                        {
                            "caption_eng": datasets.Value("string"),
                            "caption_ind": datasets.Value("string"),
                        }
                    ]
                }
            )
        elif self.config.schema == f"seacrowd_{self.SEACROWD_SCHEMA_NAME}":
            features = schemas.image_text_features(label_names=list(self.IMAGE_CLASS.values()))

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        # expect several minutes to download image data ~1.2GB
        data_path = dl_manager.download_and_extract(_URLS)

        # working with image dataset
        image_meta = Path(data_path["image"]) / "CUB_200_2011" / "images.txt"
        df_image = pd.read_csv(image_meta, sep=" ", names=["image_id", "image_path"])
        df_image['image_path'] = df_image['image_path'].apply(lambda x: Path(image_meta.parent, 'images', x))

        label_meta = Path(data_path["image"]) / "CUB_200_2011" / "image_class_labels.txt"
        df_label = pd.read_csv(label_meta, sep=" ", names=["image_id", "class_id"])

        # working with text dataset
        text_path = Path(data_path["text"])
        with open(text_path, "r") as f:
            text_data = json.load(f)

        df_text = pd.DataFrame([
            {
                'image_name': item['filename'],
                'en_caption': caption['english'],
                'id_caption': caption['indo']
            } for item in text_data['dataset'] for caption in item['captions']
        ])
        grouped_text = df_text.groupby('image_name').agg(list).reset_index()

        # working with split
        split_dir = Path(data_path["image"]) / "CUB_200_2011" / "train_test_split.txt"
        df_split = pd.read_csv(split_dir, sep=" ", names=["image_id", "is_train"])

        # merge all data
        df_image['image_name'] = df_image['image_path'].apply(lambda x: x.name)
        df = pd.merge(df_image, grouped_text, on="image_name")
        df.drop(columns=['image_name'], inplace=True)

        df = pd.merge(df, df_label, on="image_id")
        df = pd.merge(df, df_split, on="image_id")

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "data": df[df['is_train'] == 1],
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "data": df[df['is_train'] == 0],
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, data: pd.DataFrame, split: str) -> Tuple[int, Dict]:
        if self.config.schema == "source":
            for key, row in data.iterrows():
                example = {
                    "image_id": row["image_id"],
                    "class_id": row["class_id"],
                    "image_path": row["image_path"],
                    "class_name": self.IMAGE_CLASS[row["class_id"]],
                    "captions": [
                        {
                            "caption_eng": row["en_caption"][i],
                            "caption_ind": row["id_caption"][i],
                        } for i in range(len(row["en_caption"]))
                    ]
                }
                yield key, example
        elif self.config.schema == f"seacrowd_{self.SEACROWD_SCHEMA_NAME}":
            key = 0
            for _, row in data.iterrows():
                for i in range(len(row["id_caption"])):
                    example = {
                        "id": str(key),
                        "image_paths": [row["image_path"]],
                        "texts": row["id_caption"][i],
                        "metadata": {
                            "context": row["en_caption"][i],
                            "labels": [self.IMAGE_CLASS[row["class_id"]]],
                        }
                    }
                    yield key, example
                    key += 1