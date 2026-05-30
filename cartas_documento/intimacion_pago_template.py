"""
Generador de Cartas Documento de Intimación de Pago
Conforme a normativas de Derecho Comercial Argentino
"""

from datetime import datetime, timedelta
from typing import Optional


class CartaDocumentoIntimacion:
    """
    Clase para generar cartas documento de intimación de pago
    conforme a la ley argentina (Código Civil y Comercial Unificado)
    """
    
    def __init__(
        self,
        acreedor: str,
        deudor: str,
        monto: float,
        motivo: str,
        fecha_vencimiento: str,
        plazo_dias_habiles: int = 10,
        domicilio_acreedor: Optional[str] = None,
        domicilio_deudor: Optional[str] = None,
        referencia_remitos: Optional[str] = None,
    ):
        """
        Inicializa los datos de la intimación.
        
        Args:
            acreedor: Nombre del acreedor
            deudor: Nombre del deudor
            monto: Monto adeudado en pesos argentinos
            motivo: Motivo de la deuda
            fecha_vencimiento: Fecha de vencimiento original (formato: "mes de año")
            plazo_dias_habiles: Plazo para pagar en días hábiles
            domicilio_acreedor: Domicilio del acreedor
            domicilio_deudor: Domicilio del deudor
            referencia_remitos: Referencia a remitos impagos
        """
        self.acreedor = acreedor
        self.deudor = deudor
        self.monto = monto
        self.motivo = motivo
        self.fecha_vencimiento = fecha_vencimiento
        self.plazo_dias_habiles = plazo_dias_habiles
        self.domicilio_acreedor = domicilio_acreedor
        self.domicilio_deudor = domicilio_deudor
        self.referencia_remitos = referencia_remitos
        self.fecha_expedicion = datetime.now()
    
    def _calcular_fecha_vencimiento_intimacion(self) -> str:
        """Calcula la fecha de vencimiento aproximada (10 días hábiles)"""
        # Cálculo simplificado: 10 días hábiles ≈ 14 días calendario
        fecha_vencimiento = self.fecha_expedicion + timedelta(days=14)
        return fecha_vencimiento.strftime("%d de %B de %Y").replace(
            "January", "enero"
        ).replace(
            "February", "febrero"
        ).replace(
            "March", "marzo"
        ).replace(
            "April", "abril"
        ).replace(
            "May", "mayo"
        ).replace(
            "June", "junio"
        ).replace(
            "July", "julio"
        ).replace(
            "August", "agosto"
        ).replace(
            "September", "septiembre"
        ).replace(
            "October", "octubre"
        ).replace(
            "November", "noviembre"
        ).replace(
            "December", "diciembre"
        )
    
    def generar_carta(self) -> str:
        """Genera la carta documento completa"""
        
        fecha_actual = self.fecha_expedicion.strftime("%d de %B de %Y").replace(
            "January", "enero"
        ).replace(
            "February", "febrero"
        ).replace(
            "March", "marzo"
        ).replace(
            "April", "abril"
        ).replace(
            "May", "mayo"
        ).replace(
            "June", "junio"
        ).replace(
            "July", "julio"
        ).replace(
            "August", "agosto"
        ).replace(
            "September", "septiembre"
        ).replace(
            "October", "octubre"
        ).replace(
            "November", "noviembre"
        ).replace(
            "December", "diciembre"
        )
        
        fecha_vencimiento_intimacion = self._calcular_fecha_vencimiento_intimacion()
        
        monto_formateado = f"${self.monto:,.2f}".replace(",", ".")
        
        carta = f"""
CARTA DOCUMENTO DE INTIMACIÓN DE PAGO

Fecha de expedición: {fecha_actual}

DE: {self.acreedor}
{f"Domicilio: {self.domicilio_acreedor}" if self.domicilio_acreedor else ""}

PARA: {self.deudor}
{f"Domicilio: {self.domicilio_deudor}" if self.domicilio_deudor else ""}

_________________________________________________________________________________

ASUNTO: INTIMACIÓN DE PAGO

_________________________________________________________________________________

Por este medio, me dirijo a Ud. en carácter de representante de {self.acreedor}, 
a fin de INTIMAR el pago de la suma de {monto_formateado} (pesos argentinos), 
por concepto de {self.motivo}.

FUNDAMENTACIÓN LEGAL:

La presente intimación se cursa conforme a lo dispuesto por el Código Civil y 
Comercial de la Nación Argentina, particularmente los artículos referidos a 
incumplimiento de obligaciones comerciales.

ANTECEDENTES:

De acuerdo con la documentación obrante en poder de {self.acreedor}, la deuda 
tiene origen en {self.motivo}. Los comprobantes (remitos) de la prestación fueron 
emitidos con vencimiento en {self.fecha_vencimiento}.

{f"Referencia de remitos: {self.referencia_remitos}" if self.referencia_remitos else ""}

DEUDA RECLAMADA:

Monto principal: {monto_formateado}

PLAZO DE INTIMACIÓN:

Conforme a los usos mercantiles y a las normas de procedimiento comercial, 
se otorga un plazo de {self.plazo_dias_habiles} (diez) días hábiles contados 
a partir de la recepción de la presente, para que efectúe el pago de la 
totalidad de la deuda.

FECHA LÍMITE: {fecha_vencimiento_intimacion}

CONSECUENCIAS DEL INCUMPLIMIENTO:

Ante el incumplimiento de esta intimación, se procedrá conforme a derecho, 
lo que podrá incluir:

a) Acciones judiciales ejecutivas o ordinarias, según corresponda;
b) Intereses moratorios conforme a la tasa establecida por el Banco Central 
   de la República Argentina;
c) Costas y honorarios profesionales;
d) Cualquier otra acción legal que proteja los derechos de {self.acreedor}.

FORMA DE PAGO:

El pago deberá realizarse mediante transferencia bancaria, depósito en cuenta 
o cualquier otro medio que sea aceptado por {self.acreedor}.

Se requiere confirmación de pago a la presente carta.

NOTIFICACIÓN:

Conforme a lo establecido en el Código Civil y Comercial de la Nación, esta 
carta documento constituye una notificación válida y fehaciente al deudor.

_________________________________________________________________________________

Se advierte que la falta de pago en el plazo establecido constituirá 
incumplimiento de obligación comercial y habilitará el ejercicio de las 
acciones judiciales correspondientes, con todos sus efectos legales.

_________________________________________________________________________________

Atentamente,

{self.acreedor}

NOTA: Esta carta documento debe ser enviada por servicio de correo certificado 
o equivalente para asegurar constancia de entrega y fecha de notificación.

_________________________________________________________________________________
GENERADO CONFORME A NORMATIVAS ARGENTINAS DE DERECHO COMERCIAL
"""
        
        return carta
    
    def guardar_carta(self, nombre_archivo: str = None) -> str:
        """
        Guarda la carta en un archivo de texto.
        
        Args:
            nombre_archivo: Nombre del archivo (opcional)
            
        Returns:
            Ruta del archivo guardado
        """
        if not nombre_archivo:
            fecha_str = self.fecha_expedicion.strftime("%Y%m%d")
            nombre_archivo = f"carta_intimacion_{fecha_str}.txt"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(self.generar_carta())
        
        return nombre_archivo


# Ejemplo de uso
if __name__ == "__main__":
    # Datos del caso
    carta = CartaDocumentoIntimacion(
        acreedor="SIS Drogería S.R.L",
        deudor="Hospital Municipal de Santa Rosa",
        monto=260000000,
        motivo="Remitos impagos por provisión de medicamentos e insumos médicos",
        fecha_vencimiento="junio de 2024",
        plazo_dias_habiles=10,
        domicilio_deudor="Santa Rosa, La Pampa",
        referencia_remitos="Múltiples remitos entre enero y junio de 2024"
    )
    
    # Generar y mostrar la carta
    print(carta.generar_carta())
    
    # Guardar la carta
    archivo = carta.guardar_carta()
    print(f"\nCarta guardada en: {archivo}")
