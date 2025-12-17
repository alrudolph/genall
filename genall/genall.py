from __future__ import annotations

from pathlib import Path

from .codegen import generate_all, generate_import
from .parsing import File, PythonObject


class GenAll:

    def __init__(self, base_path: Path) -> None:
        self._base_path = base_path
        self._all_objs: list[PythonObject] = []
        self._initialized = False

    def write_to_file(self) -> None:
        for dir in self._sub_dirs:
            dir.write_to_file()

        items: list[tuple[str, str]] = []

        for obj in self.all_objs:
            rel = obj._file._path.relative_to(self._base_path)
            parts = rel.parts

            if len(parts) == 1:
                p = rel.stem
            else:
                p = parts[0]

            items.append((p, obj._name))

        imports: list[str] = []

        for item in items:
            imports.append(generate_import(*item))

        imp = "\n".join(imports)
        code = generate_all([i[1] for i in items])

        file_contents = f"{imp}\n\n{code}"

        with open(self._init_path, "w") as file:
            file.write(file_contents)

    @property
    def all_objs(self) -> list[PythonObject]:
        if not self._initialized:
            self._generate()
            self._initialized = True

        return self._all_objs

    def _generate(self) -> None:
        output: list[PythonObject] = []

        for file in self._sub_files:
            output.extend(file.get_all_objs())

        for dir in self._sub_dirs:
            output.extend(dir.all_objs)

        self._all_objs = output

    @property
    def _sub_dirs(self) -> list[GenAll]:
        # TODO: only containing python files
        return [GenAll(p) for p in self._base_path.iterdir() if not p.is_file()]

    @property
    def _sub_files(self) -> list[File]:
        # TODO: only python files
        return [File(p) for p in self._base_path.iterdir() if p.is_file()]

    @property
    def _init_path(self) -> Path:
        return self._base_path / "__init__.py"
