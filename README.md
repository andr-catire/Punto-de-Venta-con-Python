Este proyecto es una Simulación de un Sistema de Punto de Venta (POS) implementado completamente en Python 3.x con una interfaz de Línea de Comandos (CLI).

El sistema modela el flujo de trabajo de un supermercado, demostrando un sólido entendimiento de la lógica de negocio minorista, la gestión de datos estructurados (inventario) y la aplicación de algoritmos para manejar cálculos financieros y de pesaje. Este proyecto es una prueba de mi habilidad para modelar entidades del mundo real y gestionar la persistencia de datos en Python.
Modelado de Datos	Uso de estructuras de datos (listas ) para representar entidades complejas como productos con múltiples atributos (código, nombre, precio, stock, etc.).
Algoritmos de Negocio	Implementación de la Lógica de Pesaje (Balanza), permitiendo calcular el precio de productos por peso con una alta precisión.
Manejo de I/O (Input/Output)	Diseño de menús interactivos en la CLI, y uso eficiente de la entrada y salida para simular el escaneo y la generación del ticket de compra.
Persistencia de Datos	Carga y guardado de datos del inventario y la tasa de cambio en archivos locales (.txt o .csv), asegurando que la información persista entre sesiones.
Modularidad	Separación del flujo de trabajo en distintos módulos (modo_usuario / modo_admin), demostrando buenas prácticas de organización de código.
El sistema ofrece una gestión completa de transacciones y mantenimiento de inventario:

Módulo de Venta (Usuario)
Gestión de Transacciones: Simula el ciclo de vida completo de una venta, desde el inicio hasta el pago final.

Cálculo de Precios Mixto: Permite la venta de productos por unidad (escaneo) y por peso (balanza simulada).

Cálculo Financiero Avanzado: Sumatoria de subtotales y totales. Determina con precisión el cambio (vuelto) a entregar al recibir el monto de pago.

Módulo de Administración
Mantenimiento de Inventario: Acceso a funciones CRUD básicas (Crear, Actualizar, Eliminar) para modificar el stock y el precio de los productos.

Gestión de Tasas de Cambio: Permite actualizar la tasa de conversión (Ej. USD a otra divisa), mostrando la capacidad de manejar parámetros externos y configuraciones del sistema.
