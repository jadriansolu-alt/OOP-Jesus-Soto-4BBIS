# 📱 Lab 10: Automated Testing with pytest

## ✅ Estado Final del Proyecto

| Métrica | Valor |
|---------|-------|
| **Total Tests** | 39 |
| **Tests Pasando** | 39 (100%) |
| **Tiempo de Ejecución** | ~0.05s |
| **Fallos** | 0 |
| **Errores** | 0 |
| **Advertencias** | 0 |

---

## 🏗️ Estructura del Proyecto

```
Lab10/
├── app_movil.py                    # ✅ Backend móvil completo (276 líneas)
│   ├── CustomError                 # Base exception
│   ├── SuscripcionExpiradaError    # Excepción PRO expirada
│   ├── PuntosInsuficientesError    # Excepción sin fondos
│   ├── PerfilMovil                 # Clase base con OOP
│   └── PerfilPro                   # Subclase con herencia
│
├── tests/
│   └── test_app_movil.py           # ✅ Suite completa (529 líneas)
│       ├── 8 clases de testing
│       ├── 39 casos de prueba
│       └── 5 criterios técnicos cubiertos
│
├── screenshots/
│   ├── demo.py                     # ✅ Script demostrativo (153 líneas)
│   └── demo_screenshot.png         # ✅ Captura del console exitoso
│
├── docs/
│   ├── README.md                   # ✅ Documentación técnica completa
│   └── SUMMARY.md                  # ✅ Resumen ejecutivo
│
├── main.py                         # ✅ Punto de entrada principal
├── run_tests.py                    # ✅ Script para ejecutar tests
├── run_demo.py                     # ✅ Script para ejecutar demo
├── requirements.txt                # ✅ Dependencias del proyecto
└── .gitignore                      # ✅ Configuración Git

```

---

## 🎯 Cumplimiento del PDF Specification (100%)

### **Criterio 1: State Isolation** ✅
- **Fixture:** `standard_movil_profile()` - Perfil móvil estandarizado
- **Fixture:** `standard_pro_profile()` - Perfil PRO estandarizado
- **Uso en tests:** Todos los tests usan fixtures para aislamiento de estado

### **Criterio 2: Structural Integrity and Assertion Tests** ✅
- **9 tests con assertions directas** verificando atributos y operaciones
- **Validación inicial:** gemas=50, racha_dias=1, notificaciones_activas=True
- **Consistencia aritmética:** ganar_gemas + gastar_gemas = balance original

### **Criterio 3: Exception Validation (pytest.raises)** ✅
- **7 tests de excepciones** con `pytest.raises()`
- **CustomError hierarchy:** CustomError → SuscripcionExpiradaError, PuntosInsuficientesError
- **Validación completa:** negative, zero, insufficient funds, exact amount

### **Criterio 4: Parameterized Tests (@pytest.mark.parametrize)** ✅
- **12 tests parametrizados** cubriendo múltiples vectores de entrada
- **4 usuarios diferentes** con inicializaciones variadas
- **4 montos para ganar gemas** (25, 50, 100, 200)
- **4 montos para gastar gemas** (10, 30, 50, 40)

### **Criterio 5: Type and Hierarchy Verification (isinstance)** ✅
- **3 tests de herencia** verificando isinstance relationships
- **PerfilPro es instancia de PerfilMovil:** `True`
- **Métodos heredados funcionan correctamente**
- **Atributos adicionales presentes:** meses_suscripcion, es_pro

---

## 🧪 Ejecución del Proyecto

### **Opción 1: Ejecutar Tests (Recomendado)**
```bash
cd "C:\Users\Adrian\Desktop\No necesarios\Escuela\POO\Lab9_SotoLucero_JesusAdrian\Lab10"
python -m pytest tests/test_app_movil.py -v
```

**Salida esperada:**
```
============================= 39 passed in 0.05s =============================
```

### **Opción 2: Ejecutar Demo Interactiva**
```bash
cd "C:\Users\Adrian\Desktop\No necesarios\Escuela\POO\Lab9_SotoLucero_JesusAdrian\Lab10"
python screenshots/demo.py
```

### **Opción 3: Usar Scripts de Ejecución**
```bash
# Ejecutar tests usando script
python run_tests.py

# Ejecutar demo usando script
python run_demo.py
```

---

## 🎨 Principios OOP Aplicados

| Principio | Implementación | Ejemplo |
|-----------|----------------|---------|
| **Encapsulamiento** | Properties con getters/setters | `@property def gemas(self)` |
| **Herencia** | Subclase extendiendo base | `class PerfilPro(PerfilMovil):` |
| **Abstracción** | Métodos operacionales definidos | `ganar_gemas()`, `gastar_gemas()` |
| **Polimorfismo** | Mismos métodos, comportamientos distintos | `descargar_contenido_offline()` solo en PRO |

---

## 📦 Excepciones Personalizadas

| Clase | Jerarquía | Cuando se lanza | Mensaje |
|-------|-----------|-----------------|---------|
| `CustomError` | Base | - | Exception base |
| `SuscripcionExpiradaError` | CustomError | meses_suscripcion <= 0 | "La suscripción ha expirado. Acceso restringido." |
| `PuntosInsuficientesError` | CustomError | gemas < cantidad requerida | "Puntos insuficientes para la transacción" |

---

## 🚀 Comandos Rápidos

### **Ejecutar Tests**
```bash
cd "C:\Users\Adrian\Desktop\No necesarios\Escuela\POO\Lab9_SotoLucero_JesusAdrian\Lab10"
python -m pytest tests/test_app_movil.py -v
# O usando script:
python run_tests.py
```

### **Ejecutar Demo**
```bash
cd "C:\Users\Adrian\Desktop\No necesarios\Escuela\POO\Lab9_SotoLucero_JesusAdrian\Lab10"
python screenshots/demo.py
# O usando script:
python run_demo.py
```

---

## 📸 Evidencia Visual

![Demo Screenshot](bionic-attached://356c3de6.png?w=1200&h=800)

**Captura del console mostrando:**
- ✅ PerfilMovil funcionando correctamente
- ✅ PerfilPro con suscripción PRO activa
- ✅ Manejo de excepciones personalizado
- ✅ Verificación de herencia OOP
- ✅ **TODO FUNCIONA CORRECTAMENTE!**

---

## 🎯 Checklist Final

| Requisito PDF | Implementado | Evidencia |
|----------------|---------------|-----------|
| State Isolation (@pytest.fixture) | ✅ | 2 fixtures definidos |
| Structural Integrity & Assertions | ✅ | 9 tests con assert |
| Exception Validation (pytest.raises) | ✅ | 7 tests de excepciones |
| Parameterized Tests (@pytest.mark.parametrize) | ✅ | 12 tests parametrizados |
| Type & Hierarchy Verification (isinstance) | ✅ | 3 tests de herencia |
| Custom Exceptions | ✅ | 3 clases de excepción |
| OOP Principles | ✅ | Encapsulamiento, Herencia, Abstracción, Polimorfismo |
| Console Screenshot | ✅ | demo_screenshot.png |

---

## 📈 Métricas del Código

| Archivo | Líneas | Función Principal |
|---------|--------|-------------------|
| `app_movil.py` | 276 | Backend móvil con OOP y excepciones |
| `test_app_movil.py` | 529 | Suite de pruebas completa |
| `demo.py` | 153 | Demo interactiva |
| `README.md` | ~400 | Documentación técnica |
| **Total** | **~1,360** | **Sistema completo y documentado** |

---

## 🎓 Aprendizajes Clave

1. **Pytest es poderoso:** 39 tests en <0.05s con fixtures y parametrización
2. **OOP + Testing = Robustez:** Herencia bien estructurada facilita testing
3. **Excepciones personalizadas:** Control preciso de estados anómalos
4. **State isolation:** Fixtures garantizan pruebas independientes
5. **Parameterized tests:** Cubrir múltiples casos sin duplicar código

---

## 🏆 Conclusión

El proyecto **Lab 10: Automated Testing with pytest** ha sido exitosamente implementado siguiendo todas las especificaciones del documento PDF, aplicando principios de Programación Orientada a Objetos y creando una suite de pruebas automatizada completa.

### **Estado:** ✅ **39 tests passing - Sistema completamente funcional**

### **Tiempo total de ejecución:** ~0.05 segundos

### **Cobertura:** 100% de los criterios técnicos del PDF

---

## 📞 Puntos de Entrada para Extensión

### **Para agregar más funcionalidades:**

1. **Nuevos métodos en PerfilMovil/PerfilPro**
   - Ej: `can_afford_item(price)` - Verifica si puede comprar un ítem
   
2. **Más tests de integración**
   - Ej: Transacciones concurrentes, rollback de operaciones

3. **Mocking de dependencias externas**
   - Ej: Simular base de datos con pytest-mock

4. **Coverage report**
   - `pytest --cov=app_movil` para ver qué líneas se cubren

---

## 📄 Documentación Adicional

- **`docs/README.md`** - Documentación técnica completa con ejemplos y explicaciones
- **`docs/SUMMARY.md`** - Resumen ejecutivo con métricas y checklist final

---

**Última actualización:** 2026-11-09

**Estado del proyecto:** ✅ **Listo para entrega en clase**