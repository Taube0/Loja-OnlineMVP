from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import xml.etree.ElementTree as ET

router = APIRouter()

class FreteRequest(BaseModel):
    cep_destino: str

@router.post("/frete")
def calcular_frete(request: FreteRequest):
    try:
        url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx"
        params = {
            "nCdEmpresa": "",
            "sDsSenha": "",
            "nCdServico": "04014",  # SEDEX
            "sCepOrigem": "55200000",
            "sCepDestino": request.cep_destino,
            "nVlPeso": "1",
            "nCdFormato": "1",
            "nVlComprimento": "25",
            "nVlAltura": "5",
            "nVlLargura": "20",
            "nVlDiametro": "0",
            "sCdMaoPropria": "n",
            "nVlValorDeclarado": "120.00",
            "sCdAvisoRecebimento": "n",
            "StrRetorno": "xml"
        }

        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()

        xml_root = ET.fromstring(response.text)
        valor = xml_root.find(".//Valor").text.replace(",", ".")
        prazo = xml_root.find(".//PrazoEntrega").text

        return {
            "valor": valor,
            "prazo": prazo
        }

    except Exception:
        # 🔁 Fallback se os Correios falharem
        return {
            "valor": "24.90",
            "prazo": "5"
        }
