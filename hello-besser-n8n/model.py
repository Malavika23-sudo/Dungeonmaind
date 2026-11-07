"""BESSER domain model for the seminar hello world.

The seminar slides name this stack BESSER (https://besser-pearl.org)
with n8n (https://github.com/n8n-io/n8n.git) as the backend.
"""

from pathlib import Path

from besser.BUML.metamodel.structural.structural import (
    Class,
    DomainModel,
    Property,
    StringType,
)
from besser.generators.python_classes import PythonGenerator

GREETING_TEXT = "Hello, world"


def build_model() -> DomainModel:
    greeting = Class(
        name="Greeting",
        attributes={
            Property(name="text", type=StringType),
        },
    )
    return DomainModel(name="Hello", types={greeting}, associations=set())


def generate(output_dir: Path) -> DomainModel:
    model = build_model()
    output_dir.mkdir(parents=True, exist_ok=True)
    PythonGenerator(model=model, output_dir=str(output_dir)).generate()
    return model
