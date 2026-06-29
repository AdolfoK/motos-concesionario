"""Utilidades para generar el enlace de WhatsApp de una reserva."""
from urllib.parse import quote

from django.conf import settings


def construir_mensaje(reserva) -> str:
    """Arma el texto pre-llenado que el cliente envia a la concesionaria."""
    lineas = [
        "Hola! Quiero reservar una hora de servicio tecnico:",
        "",
        f"- Cliente: {reserva.nombre_cliente}",
        f"- Telefono: {reserva.telefono}",
        f"- Servicio: {reserva.get_tipo_servicio_display()}",
        f"- Fecha: {reserva.fecha.strftime('%d-%m-%Y')}",
        f"- Bloque horario: {reserva.bloque_horario}",
        f"- Moto: {reserva.moto_marca} {reserva.moto_modelo}",
    ]
    if reserva.patente:
        lineas.append(f"- Patente: {reserva.patente}")
    if reserva.comentario:
        lineas.append(f"- Comentario: {reserva.comentario}")
    lineas.append("")
    lineas.append(f"(Solicitud #{reserva.id})")
    return "\n".join(lineas)


def construir_url(reserva) -> str:
    """Devuelve el enlace wa.me con el mensaje codificado."""
    numero = settings.WHATSAPP_NUMERO
    mensaje = quote(construir_mensaje(reserva))
    return f"https://wa.me/{numero}?text={mensaje}"
