from weasyprint import HTML
import base64

# Contenido HTML para el PDF profesional
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 20mm;
            background-color: #ffffff;
            @bottom-right {
                content: "Página " counter(page);
                font-size: 9pt;
                color: #666;
            }
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
            line-height: 1.5;
            font-size: 10pt;
        }
        .header-bar {
            background-color: #0078d4;
            color: white;
            padding: 20px;
            margin: -20mm -20mm 20px -20mm;
            text-align: center;
        }
        h1 { margin: 0; font-size: 22pt; font-weight: bold; }
        h2 { color: #0078d4; border-left: 5px solid #0078d4; padding-left: 10px; margin-top: 25px; font-size: 16pt; }
        h3 { color: #005a9e; font-size: 13pt; margin-top: 15px; }
        table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 9pt; }
        th { background-color: #f2f2f2; color: #0078d4; font-weight: bold; border: 1px solid #ddd; padding: 8px; text-align: left; }
        td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
        tr:nth-child(even) { background-color: #fafafa; }
        .callout { background-color: #e7f3ff; border-radius: 5px; padding: 15px; margin: 15px 0; border: 1px solid #b3d7ff; }
        .important { color: #d83b01; font-weight: bold; }
        .footer { font-size: 8pt; color: #666; margin-top: 30px; border-top: 1px solid #eee; padding-top: 10px; }
        ul { margin: 10px 0; padding-left: 20px; }
        li { margin-bottom: 5px; }
    </style>
</head>
<body>
    <div class="header-bar">
        <h1>Azure Virtual Networking (VNet)</h1>
        <p>Guía Técnica Funcional de Arquitectura, Rendimiento y Costos (2026)</p>
    </div>

    <h2>1. Definición Funcional: El Contenedor Lógico</h2>
    <p>La <strong>VNet</strong> no es un "servicio" que se compra, es un <strong>aislamiento lógico</strong>. Es el perímetro que define quién puede hablar con quién dentro de la nube pública.</p>
    
    <table>
        <tr>
            <th>Factor</th>
            <th>Descripción Detallada</th>
        </tr>
        <tr>
            <td><strong>¿Cuándo se ocupa?</strong></td>
            <td>Siempre que un recurso (VM, Azure Function, DB) deba estar fuera del alcance del Internet público o requiera conexión con una red física (On-prem).</td>
        </tr>
        <tr>
            <td><strong>¿Por qué se ocupa?</strong></td>
            <td>Para control granular del tráfico. Permite usar IPs privadas internas (RFC 1918) y micro-segmentar la red mediante Subredes y NSGs.</td>
        </tr>
        <tr>
            <td><strong>Configuración Crítica</strong></td>
            <td><strong>Espacio de Direcciones (CIDR):</strong> El rango elegido (ej. 10.0.0.0/16) debe ser único y no traslaparse con redes locales para evitar fallos de enrutamiento.</td>
        </tr>
    </table>

    <div class="callout">
        <strong>Las 5 IPs Reservadas de Azure:</strong> En cada subred, pierdes 5 direcciones IP:
        <ul>
            <li><strong>.0:</strong> Dirección de red.</li>
            <li><strong>.1:</strong> Puerta de enlace predeterminada (Default Gateway).</li>
            <li><strong>.2 y .3:</strong> Reservadas para mapear los DNS de Azure a la VNet.</li>
            <li><strong>Última (.255 en un /24):</strong> Dirección de difusión (Broadcast).</li>
        </ul>
    </div>

    <h2>2. Ecosistema de Servicios Complementarios</h2>
    <p>Una VNet "vacía" no hace mucho. Se vuelve funcional al acoplar estos servicios:</p>
    
    <table>
        <tr>
            <th>Servicio</th>
            <th>Función Principal</th>
            <th>Impacto en Arquitectura</th>
        </tr>
        <tr>
            <td><strong>NAT Gateway</strong></td>
            <td>Centraliza la salida a Internet.</td>
            <td>Otorga una <strong>IP Pública Fija</strong> a todos los recursos de la subred, eliminando la necesidad de asignar IPs públicas a cada recurso.</td>
        </tr>
        <tr>
            <td><strong>Private DNS Zone</strong></td>
            <td>Resolución de nombres interna.</td>
            <td>Permite usar nombres como <i>"mi-db.internal"</i> en lugar de IPs, sin salir jamás a Internet.</td>
        </tr>
        <tr>
            <td><strong>Public IP (Standard)</strong></td>
            <td>Identidad externa.</td>
            <td>Es el "DNI" de tu red ante el mundo. Siempre debe ser SKU Standard en 2026 por seguridad y disponibilidad.</td>
        </tr>
        <tr>
            <td><strong>VNet Peering</strong></td>
            <td>Puente entre redes.</td>
            <td>Conecta dos VNets (incluso entre regiones) para que se vean como una sola red privada.</td>
        </tr>
    </table>

    <h2>3. Factores de Costo: ¿Qué estás pagando realmente?</h2>
    <p>La facturación de red en Azure es una combinación de costos fijos (por hora) y variables (por volumen).</p>

    <h3>A. Costos de Transferencia de Datos (Bandwidth)</h3>
    <ul>
        <li><strong>Ingreso (Ingress):</strong> 100% gratuito. Traer datos a Azure no cuesta.</li>
        <li><strong>Egreso (Egress):</strong> Gratuito los primeros 100GB/mes. A partir de ahí, cuesta aprox. <strong>$0.087 USD por GB</strong> (Zona 1: EE.UU./Europa).</li>
        <li><strong>VNet Peering (Regional):</strong> $0.01 USD por GB procesado (tanto de entrada como de salida en ambos extremos).</li>
    </ul>

    <h3>B. Componentes Activos (Costos Fijos y Procesamiento)</h3>
    <table>
        <tr>
            <th>Componente</th>
            <th>Costo Fijo (Uso Mínimo)</th>
            <th>Costo por Procesamiento</th>
        </tr>
        <tr>
            <td><strong>NAT Gateway</strong></td>
            <td>~$0.045 USD / hora (~$32.40 USD mes)</td>
            <td>$0.045 USD por cada GB de datos.</td>
        </tr>
        <tr>
            <td><strong>Public IP Static</strong></td>
            <td>~$0.005 USD / hora (~$3.60 USD mes)</td>
            <td>No aplica (se cobra la reserva del recurso).</td>
        </tr>
        <tr>
            <td><strong>VPN Gateway</strong></td>
            <td>Varía según SKU (desde ~$27 USD mes)</td>
            <td>Cobra por GB de salida hacia tu red física.</td>
        </tr>
    </table>

    <h2>4. Rendimiento y Transacciones: Límites de Capacidad</h2>
    <p>Para aplicaciones de alto tráfico (como IA generativa o grandes flujos de datos), los límites no son solo de velocidad, sino de conexiones.</p>
    <ul>
        <li><strong>Throughput de NAT Gateway:</strong> Soporta hasta <strong>100 Gbps</strong> en el nuevo SKU StandardV2 (2026). El estándar anterior es de 45 Gbps.</li>
        <li><strong>Paquetes por Segundo (PPS):</strong> NAT Gateway puede procesar hasta <strong>10 millones de PPS</strong>.</li>
        <li><strong>Puertos SNAT:</strong> Cada IP pública asociada a un NAT Gateway otorga <strong>64,512 puertos</strong> para conexiones concurrentes. Si tu aplicación abre miles de conexiones por minuto, necesitas monitorizar el "SNAT Port Exhaustion".</li>
    </ul>

    <div class="callout">
        <strong>Resumen de Factores de Cobro Críticos:</strong>
        <br>1. <strong>Tiempo:</strong> Los Gateways e IPs cobran por segundo de existencia, no solo por uso.
        <br>2. <strong>Volumen:</strong> El NAT Gateway cobra tanto por los datos que <i>salen</i> como por los que <i>regresan</i> como respuesta.
        <br>3. <strong>Saltos:</strong> Si los datos pasan de una VNet a otra vía Peering y luego salen por un NAT, pagas el Peering + el Procesamiento NAT + el Egreso a Internet.
    </div>

    <div class="footer">
        Este documento es para fines de capacitación técnica. Los precios son estimados basados en tarifas globales de Azure para 2026.
    </div>
</body>
</html>
"""

# Generación del PDF
input_html_path = "guia_vnet.html"
output_pdf_path = "Guia_Maestra_Azure_Networking_2026.pdf"

with open(input_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

HTML(filename=input_html_path).write_pdf(output_pdf_path)