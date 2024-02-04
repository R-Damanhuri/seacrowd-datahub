# coding=utf-8
# Copyright 2022 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from typing import Dict, List, Tuple

import datasets
import pandas as pd

from seacrowd.utils import schemas
from seacrowd.utils.configs import SEACrowdConfig
from seacrowd.utils.constants import TASK_TO_SCHEMA, Licenses, Tasks

_CITATION = """\
@inproceedings{mazumder2021multilingual,
  title={Multilingual Spoken Words Corpus},
  author={Mazumder, Mark and Chitlangia, Sharad and Banbury, Colby and Kang, Yiping and Ciro, Juan Manuel and Achorn, Keith and Galvez, Daniel and Sabini, Mark and Mattson, Peter and Kanter, David and others},
  booktitle={Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)},
  year={2021}
}
"""

_DATASETNAME = "mswc"

_DESCRIPTION = """\
Multilingual Spoken Words Corpus is a large and growing audio dataset of spoken words in 50 languages collectively spoken by over 5 billion people, for academic research and commercial applications in keyword spotting and spoken term search, licensed under CC-BY 4.0. The dataset contains more than 340,000 keywords, totaling 23.4 million 1-second spoken examples (over 6,000 hours). The dataset has many use cases, ranging from voice-enabled consumer devices to call center automation. This dataset is generated by applying forced alignment on crowd-sourced sentence-level audio to produce per-word timing estimates for extraction. All alignments are included in the dataset.
"""

_HOMEPAGE = "https://huggingface.co/datasets/MLCommons/ml_spoken_words"

_LANGUAGES = ["cnh", "ind", "vie"]  # We follow ISO639-3 language code (https://iso639-3.sil.org/code_tables/639/data)

_LICENSE = Licenses.CC_BY_4_0.value

_LOCAL = False

_URLS = {
    _DATASETNAME: {
        "train": [
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/cnh_wav/train/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/cnh_opus/train/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/ind_wav/train/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/ind_opus/train/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/vie_wav/train/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/vie_opus/train/0000.parquet?download=true"
        ],

        "validation": [
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/cnh_wav/validation/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/cnh_opus/validation/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/ind_wav/validation/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/ind_opus/validation/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/vie_wav/validation/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/vie_opus/validation/0000.parquet?download=true",
        ],

        "test": [
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/cnh_wav/test/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/cnh_opus/test/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/ind_wav/test/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/ind_opus/test/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/vie_wav/test/0000.parquet?download=true",
            "https://huggingface.co/datasets/MLCommons/ml_spoken_words/resolve/refs%2Fconvert%2Fparquet/vie_opus/test/0000.parquet?download=true",
        ],
    },
}

_SUPPORTED_TASKS = [Tasks.SPEECH_RECOGNITION]
_SUPPORTED_SCHEMA_STRINGS = [f"seacrowd_{str(TASK_TO_SCHEMA[task]).lower()}" for task in _SUPPORTED_TASKS]

_SOURCE_VERSION = "1.0.0"

_SEACROWD_VERSION = "1.0.0"


class MSWC(datasets.GeneratorBasedBuilder):
    """Multilingual Spoken Words Corpus is a large and growing audio dataset of spoken words in 50 languages collectively spoken by over 5 billion people, for academic research and commercial applications in keyword spotting and spoken term search, licensed under CC-BY 4.0."""

    SOURCE_VERSION = datasets.Version(_SOURCE_VERSION)
    SEACROWD_VERSION = datasets.Version(_SEACROWD_VERSION)

    BUILDER_CONFIGS = [
        SEACrowdConfig(
            name=f"{_DATASETNAME}_source",
            version=SOURCE_VERSION,
            description=f"{_DATASETNAME} source schema",
            schema="source",
            subset_id=f"{_DATASETNAME}",
        ),
    ]

    seacrowd_schema_config: list[SEACrowdConfig] = []

    for seacrowd_schema in _SUPPORTED_SCHEMA_STRINGS:

        seacrowd_schema_config.append(
            SEACrowdConfig(
                name=f"{_DATASETNAME}_{seacrowd_schema}",
                version=SEACROWD_VERSION,
                description=f"{_DATASETNAME} {seacrowd_schema} schema",
                schema=f"{seacrowd_schema}",
                subset_id=f"{_DATASETNAME}",
            )
        )

    BUILDER_CONFIGS.extend(seacrowd_schema_config)

    DEFAULT_CONFIG_NAME = f"{_DATASETNAME}_source"

    def _info(self) -> datasets.DatasetInfo:

        if self.config.schema == "source":
            features = datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "is_valid": datasets.Value("bool"),
                    "language": datasets.ClassLabel(num_classes=3),
                    "speaker_id": datasets.Value("string"),
                    "gender": datasets.ClassLabel(num_classes=3),
                    "keyword": datasets.Value("string"),
                    "audio": datasets.Audio()
                }
            )

        elif self.config.schema == f"seacrowd_{str(TASK_TO_SCHEMA[Tasks.SPEECH_RECOGNITION]).lower()}":
            features = schemas.speech_text_features

        else:
            raise ValueError(f"Invalid config: {self.config.name}")

        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        """Returns SplitGenerators."""

        split_names = ["train", "validation", "test"]

        result = []

        for split_name in split_names:
            paths = dl_manager.download_and_extract(_URLS[_DATASETNAME][split_name])

            result.append([
                datasets.SplitGenerator(
                    name=split_name,
                    gen_kwargs={
                        "paths": paths,
                    },
                ),
            ])

        return result

    def _generate_examples(self, paths: list[Path]) -> Tuple[int, Dict]:
        """Yields examples as (key, example) tuples."""

        is_schema_found = False
        idx = 0

        if self.config.schema == "source":
            is_schema_found = True

            for path in paths:
                df = pd.read_parquet(path)

                for _, row in df.iterrows():
                    yield idx, row.to_dict()
                    idx += 1

        else:
            for seacrowd_schema in _SUPPORTED_SCHEMA_STRINGS:
                if self.config.schema == seacrowd_schema:
                    is_schema_found = True

                    for path in paths:
                        df = pd.read_parquet(path)
                        
                        # TODO: modify df

                        for _, row in df.iterrows():
                            yield idx, row.to_dict()
                            idx += 1

        if not is_schema_found:
            raise ValueError(f"Invalid config: {self.config.name}")

# This allows you to run your dataloader with `python [dataset_name].py` during development
# TODO: Remove this before making your PR
if __name__ == "__main__":
    datasets.load_dataset(__file__, "mswc_source")