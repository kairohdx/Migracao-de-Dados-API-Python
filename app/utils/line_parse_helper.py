from datetime import datetime
from app.models.schemas.parsed_line.parsed_line import ParsedLine


class LineParseHelper:
    @staticmethod
    def parse_line(line):
        """
        Parseia uma linha de 95 caracteres em intervalos específicos
        Retorna um dicionário com os valores convertidos
        """
        if len(line) != 95:
            raise ValueError("A linha deve ter exatamente 95 caracteres")
        #0000000070                              Palmer Prosacco00000007530000000003     1836.7420210308
        return ParsedLine(
            user_id=int(line[0:10].strip()),
            user_name=line[10:55].strip(),
            order_id=int(line[55:65].strip()),
            product_id=int(line[65:75].strip()),
            order_value=line[75:87].strip(),
            order_date=datetime.strptime(line[87:95].strip(), "%Y%m%d").date()
        )