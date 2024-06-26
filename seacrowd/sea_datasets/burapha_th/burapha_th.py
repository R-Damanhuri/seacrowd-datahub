import os
from pathlib import Path
from typing import Dict, List, Tuple

import datasets

from seacrowd.utils import schemas
from seacrowd.utils.configs import SEACrowdConfig
from seacrowd.utils.constants import Licenses, Tasks

_CITATION = """\
@Article{app12084083,
AUTHOR = {Onuean, Athita and Buatoom, Uraiwan and Charoenporn, Thatsanee and Kim, Taehong and Jung, Hanmin},
TITLE = {Burapha-TH: A Multi-Purpose Character, Digit, and Syllable Handwriting Dataset},
JOURNAL = {Applied Sciences},
VOLUME = {12},
YEAR = {2022},
NUMBER = {8},
ARTICLE-NUMBER = {4083},
URL = {https://www.mdpi.com/2076-3417/12/8/4083},
ISSN = {2076-3417},
DOI = {10.3390/app12084083}
}
"""
_DATASETNAME = "burapha_th"

_DESCRIPTION = """\
The dataset has 68 character classes, 10 digit classes, and 320 syllable classes.
For constructing the dataset, 1072 Thai native speakers wrote on collection datasheets
that were then digitized using a 300 dpi scanner.
De-skewing, detection box and segmentation algorithms were applied to the raw scans
for image extraction. The dataset, unlike all other known Thai handwriting datasets, retains
existing noise, the white background, and all artifacts generated by scanning.
"""

_HOMEPAGE = "https://services.informatics.buu.ac.th/datasets/Burapha-TH/"

_LICENSE = Licenses.UNKNOWN.value

_LOCAL = False
_LANGUAGES = ["tha"]  # We follow ISO639-3 language code (https://iso639-3.sil.org/code_tables/639/data)

_URLS = {
    "character": {"test": "https://services.informatics.buu.ac.th/datasets/Burapha-TH/character/20210306-test.zip", "train": "https://services.informatics.buu.ac.th/datasets/Burapha-TH/character/20210306-train.zip"},
    "digit": {"test": "https://services.informatics.buu.ac.th/datasets/Burapha-TH/digit/20210307-test.zip", "train": "https://services.informatics.buu.ac.th/datasets/Burapha-TH/digit/20210307-train.zip"},
    "syllable": {"test": "https://services.informatics.buu.ac.th/datasets/Burapha-TH/syllable/20210309-test-ori.zip", "train": "https://services.informatics.buu.ac.th/datasets/Burapha-TH/syllable/20210309-train-ori.zip"},
}

_SUPPORTED_TASKS = [Tasks.IMAGE_CAPTIONING]
_SOURCE_VERSION = "1.0.0"

_SEACROWD_VERSION = "2024.06.20"

_SUBSETS = ["character", "digit", "syllable"]


def config_constructor(subset: str, schema: str, version: str) -> SEACrowdConfig:
    return SEACrowdConfig(
        name=f"{_DATASETNAME}_{subset}_{schema}",
        version=version,
        description=f"{_DATASETNAME} {subset} {schema} schema",
        schema=f"{schema}",
        subset_id=f"{_DATASETNAME}_{subset}",
    )


class BuraphaThDataset(datasets.GeneratorBasedBuilder):
    """
    The dataset has 68 character classes, 10 digit classes, and 320 syllable classes.
    For constructing the dataset, 1072 Thai native speakers wrote on collection datasheets
    that were then digitized using a 300 dpi scanner.
    De-skewing, detection box and segmentation algorithms were applied to the raw scans for
    image extraction. The dataset, unlike all other known Thai handwriting datasets, retains
    existing noise, the white background, and all artifacts generated by scanning.
    """

    BUILDER_CONFIGS = [config_constructor(subset, "source", _SOURCE_VERSION) for subset in _SUBSETS]
    BUILDER_CONFIGS.extend([config_constructor(subset, "seacrowd_imtext", _SEACROWD_VERSION) for subset in _SUBSETS])

    DEFAULT_CONFIG_NAME = f"{_DATASETNAME}_digit_source"

    label_chr_dig = [str(i).zfill(2) for i in range(78)]
    label_syl = [str(i).zfill(3) for i in range(320)]

    def _info(self) -> datasets.DatasetInfo:
        task = self.config.subset_id.split("_")[2]
        if self.config.schema == "source":
            features = datasets.Features(
                {"id": datasets.Value("string"), "image_paths": datasets.Value("string"), "label": datasets.Sequence(datasets.ClassLabel(names=self.label_chr_dig if task == "character" or task == "digit" else self.label_syl))}
            )
        elif self.config.schema == "seacrowd_imtext":
            features = schemas.image_text_features(label_names=self.label_chr_dig if task == "character" or task == "digit" else self.label_syl)
        else:
            raise NotImplementedError()

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        """Returns SplitGenerators."""

        task = self.config.subset_id.split("_")[2]

        _local_path = dl_manager.download_and_extract(_URLS[task])
        train_path, test_path = _local_path["train"], _local_path["test"]
        if task in ["character", "digit"]:
            train_path = os.path.join(train_path, "train")
            test_path = os.path.join(test_path, "test")
        # for "syllable" type task
        else:
            train_path = os.path.join(train_path, "train-ori")
            test_path = os.path.join(test_path, "test-ori")

        data_pair = {}

        for dir_name in os.listdir(train_path):
            dir_name_split = dir_name.split("-")
            file_names = []

            for file_name in os.listdir(os.path.join(train_path, dir_name)):
                file_names.append(os.path.join(train_path, dir_name, file_name))

            label = dir_name_split[0]
            data_pair[label] = file_names

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_pair,
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "filepath": data_pair,
                    "split": "test",
                },
            ),
        ]

    def _generate_examples(self, filepath: Path, split: str) -> Tuple[int, Dict]:
        """Yields examples as (key, example) tuples."""
        task = self.config.subset_id.split("_")[2]
        counter = 0

        for key, imgs in filepath.items():
            for img in imgs:
                if self.config.schema == "source":
                    yield counter, {"id": str(counter), "image_paths": img, "label": [self.label_chr_dig.index(key) if task == "character" or task == "digit" else self.label_syl.index(key)]}
                elif self.config.schema == "seacrowd_imtext":
                    yield counter, {
                        "id": str(counter),
                        "image_paths": [img],
                        "texts": None,
                        "metadata": {
                            "context": None,
                            "labels": [self.label_chr_dig.index(key) if task in ["character", "digit"] else self.label_syl.index(key)],
                        },
                    }
                counter += 1
