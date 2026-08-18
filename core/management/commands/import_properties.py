import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from core.models import Property


class Command(BaseCommand):
    help = "Importa rapidamente a base organizada de anúncios."

    def add_arguments(self, parser):
        parser.add_argument("--file", default=str(Path("data") / "imoveis.csv"))
        parser.add_argument("--clear", action="store_true")

    @staticmethod
    def parse_price(value):
        raw = (value or "").strip().replace("€", "").replace(" ", "")
        if not raw:
            return None
        if "," in raw and "." in raw:
            raw = raw.replace(".", "").replace(",", ".")
        else:
            raw = raw.replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            return None

    def handle(self, *args, **opts):
        path = Path(opts["file"])
        if not path.exists():
            self.stderr.write(self.style.ERROR(f"CSV não encontrado: {path}"))
            return

        if opts["clear"]:
            self.stdout.write("A limpar a base antiga...")
            Property.objects.all().delete()

        objects = []
        seen_links = set()

        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                link = (row.get("Link") or "").strip()

                # A base de publicação já é única por Link.
                # Evita duplicações caso o CSV seja alterado no futuro.
                if link and link in seen_links:
                    continue
                if link:
                    seen_links.add(link)

                objects.append(Property(
                    title=(row.get("Título Limpo") or row.get("Título") or "").strip(),
                    address=(row.get("Endereço") or "").strip(),
                    district=(row.get("Distrito") or "").strip(),
                    municipality=(row.get("Concelho") or "").strip(),
                    parish=(row.get("Freguesia") or "").strip(),
                    location=(row.get("Localização") or "").strip(),
                    price=self.parse_price(row.get("Preço")),
                    typology=(row.get("Tipologia") or "").strip(),
                    bathrooms=(row.get("Casas de Banho") or "").strip(),
                    description=(row.get("Descrição") or "").strip(),
                    features=(row.get("Características") or "").strip(),
                    gallery=(row.get("Galeria") or "").strip(),
                    source_link=link,
                ))

        self.stdout.write(f"A importar {len(objects):,} anúncios em lote...")
        Property.objects.bulk_create(objects, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            f"Importação concluída. Total: {Property.objects.count():,} anúncios."
        ))
