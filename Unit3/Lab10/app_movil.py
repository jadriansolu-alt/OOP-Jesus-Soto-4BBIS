"""
Lab 10: Automated Testing with pytest - Mobile System Backend
Objet-Oriented Programming (OOP) Paradigm

This module implements a mobile system backend managing user profiles
and business rules, incorporating custom exceptions for anomalous states.
"""


# ============================================================================
# 1. DOMAIN EXCEPTION HIERARCHY
# ============================================================================

class CustomError(Exception):
    """Base class for all custom exceptions in the mobile system."""
    pass


class SuscripcionExpiradaError(CustomError):
    """Raised when attempting to execute restricted operations without an active membership."""
    
    def __init__(self, message="La suscripción ha expirado. Acceso restringido.", user=None):
        self.message = message
        self.user = user
        super().__init__(f"{user}: {message}" if user else message)


class PuntosInsuficientesError(CustomError):
    """Raised when a transaction exceeds the available gem balance."""
    
    def __init__(self, message="Puntos insuficientes para la transacción.", required=0, available=0):
        self.message = message
        self.required = required
        self.available = available
        super().__init__(f"{message} (Necesitas: {required}, Tienes: {available})")


# ============================================================================
# 2. BASE CLASS: PerfilMovil
# ============================================================================

class PerfilMovil:
    """
    Base class for mobile user profiles.
    
    Instance Attributes:
        username (string): User's unique identifier
        gemas (integer, initial nominal value of 50; requires strict validation against negative values)
        racha_dias (integer, initial value of 1)
        notificaciones_activas (boolean, default value True)
    
    Operational Methods:
        ganar_gemas(cantidad: int) -> int: Increments the accumulated balance. Must validate that 
            the input parameter is strictly positive (raises ValueError otherwise).
        gastar_gemas(cantidad: int) -> int: Decrements the balance after verifying availability. 
            Validates positive value restrictions and sufficiency of funds (raises ValueError or 
            PuntosInsuficientesError accordingly).
    """
    
    def __init__(self, username: str, gemas: int = 50, racha_dias: int = 1, notificaciones_activas: bool = True):
        """
        Initialize a mobile user profile.
        
        Args:
            username: User's unique identifier string
            gemas: Initial gem balance (default 50)
            racha_dias: Current streak days (default 1)
            notificaciones_activas: Whether notifications are active (default True)
            
        Raises:
            ValueError: If gemas is negative or racha_dias is invalid
        """
        
        # Strict validation against negative values for gemas
        if gemas < 0:
            raise ValueError(f"El balance de gemas no puede ser negativo. Inicial: {gemas}")
        
        self.username = username
        self._gemas = gemas
        self.racha_dias = racha_dias
        self.notificaciones_activas = notificaciones_activas
    
    @property
    def gemas(self):
        """Get the current gem balance."""
        return self._gemas
    
    @property
    def username(self):
        """Get the user's unique identifier."""
        return self._username
    
    @username.setter
    def username(self, value: str):
        """Set the user's unique identifier with validation."""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("El username debe ser una cadena no vacía")
        self._username = value.strip()
    
    def ganar_gemas(self, cantidad: int) -> int:
        """
        Increment the accumulated gem balance.
        
        Args:
            cantidad: Number of gems to add (must be strictly positive)
            
        Returns:
            The new total gem balance
            
        Raises:
            ValueError: If cantidad is not strictly positive
        """
        if cantidad <= 0:
            raise ValueError(f"La cantidad de gemas a ganar debe ser estrictamente positiva. Recibido: {cantidad}")
        
        self._gemas += cantidad
        return self._gemas
    
    def gastar_gemas(self, cantidad: int) -> int:
        """
        Decrement the balance after verifying availability.
        
        Args:
            cantidad: Number of gems to spend (must be positive and available)
            
        Returns:
            The new total gem balance
            
        Raises:
            ValueError: If cantidad is not strictly positive
            PuntosInsuficientesError: If insufficient gems are available
        """
        # Validate positive value restriction
        if cantidad <= 0:
            raise ValueError(f"La cantidad de gemas a gastar debe ser estrictamente positiva. Recibido: {cantidad}")
        
        # Verify sufficiency of funds
        if self._gemas < cantidad:
            raise PuntosInsuficientesError(
                message="Puntos insuficientes para la transacción",
                required=cantidad,
                available=self._gemas
            )
        
        self._gemas -= cantidad
        return self._gemas
    
    def __str__(self):
        """String representation of the profile."""
        status = "Activa" if self.notificaciones_activas else "Inactiva"
        return f"PerfilMovil(username='{self.username}', gemas={self._gemas}, racha_dias={self.racha_dias}, notificaciones={status})"


# ============================================================================
# 3. DERIVED SUBCLASS: PerfilPro
# ============================================================================

class PerfilPro(PerfilMovil):
    """
    Derived class for PRO users with premium subscription benefits.
    
    Inheritance and Polymorphism: Extends the PerfilMovil class.
    
    Additional Attributes:
        meses_suscripcion (integer): Number of months in current subscription
        es_pro (boolean, True): Indicates this is a PRO profile
        
    Validates that the initial period is greater than zero (raises ValueError).
    
    Specialized Method:
        descargar_contenido_offline() -> str: Evaluates temporal validity. 
            If the months expire to 0, it switches the state to es_pro = False 
            and propagates the SuscripcionExpiradaError exception; otherwise, 
            it confirms successful execution.
    """
    
    def __init__(self, username: str, gemas: int = 50, racha_dias: int = 1, 
                 notificaciones_activas: bool = True, meses_suscripcion: int = 3):
        """
        Initialize a PRO user profile.
        
        Args:
            username: User's unique identifier string
            gemas: Initial gem balance (default 50)
            racha_dias: Current streak days (default 1)
            notificaciones_activas: Whether notifications are active (default True)
            meses_suscripcion: Number of months in current subscription
            
        Raises:
            ValueError: If any inherited attribute is invalid or if meses_suscripcion <= 0
        """
        
        # Call parent constructor with validation
        super().__init__(username, gemas, racha_dias, notificaciones_activas)
        
        # Validate initial period is greater than zero
        if meses_suscripcion <= 0:
            raise ValueError(f"El periodo de suscripción debe ser mayor a cero. Inicial: {meses_suscripcion}")
        
        self.meses_suscripcion = meses_suscripcion
        self.es_pro = True
    
    @property
    def meses_suscripcion(self):
        """Get the number of months in current subscription."""
        return self._meses_suscripcion
    
    @meses_suscripcion.setter
    def meses_suscripcion(self, value: int):
        """Set subscription months with validation (must be > 0 for normal operation).
        
        Note: Can be set to 0 temporarily to simulate expired subscription for testing.
        """
        # Allow 0 only if current state is also 0 (transitioning from active to expired)
        if value < 0:
            raise ValueError(f"Los meses de suscripción no pueden ser negativos. Asignado: {value}")
        self._meses_suscripcion = value
    
    def descargar_contenido_offline(self) -> str:
        """
        Evaluate temporal validity of the PRO subscription for offline content download.
        
        Returns:
            Success message string
            
        Raises:
            ValueError: If initial period is not greater than zero (inherited validation)
            SuscripcionExpiradaError: If months expire to 0, switches state and raises exception
        """
        # Check if subscription has expired
        if self.meses_suscripcion <= 0:
            # Switch the state to es_pro = False
            self.es_pro = False
            raise SuscripcionExpiradaError(user=self.username)
        
        # Successful execution - confirm with message
        return f"Descarga exitosa para usuario '{self.username}'. " \
               f"Suscripción PRO activa: {self.meses_suscripcion} meses restantes. " \
               f"Gemas disponibles: {self._gemas}"
    
    def __str__(self):
        """String representation of the PRO profile."""
        status = "Activa" if self.es_pro else "Expirada"
        notif_status = "Activa" if self.notificaciones_activas else "Inactiva"
        return f"PerfilPro(username='{self.username}', gemas={self._gemas}, racha_dias={self.racha_dias}, " \
               f"suscripcion={status} ({self.meses_suscripcion} meses), notificaciones={notif_status})"


# ============================================================================
# 4. UTILITY FUNCTIONS FOR TESTING
# ============================================================================

def create_standard_profile(username: str = "test_user") -> PerfilMovil:
    """
    Create a standardized PerfilMovil instance for testing.
    
    Args:
        username: Username for the profile (default "test_user")
        
    Returns:
        A new PerfilMovil instance with default values
    """
    return PerfilMovil(username=username, gemas=50, racha_dias=1, notificaciones_activas=True)


def create_standard_pro_profile(username: str = "pro_test_user") -> PerfilPro:
    """
    Create a standardized PerfilPro instance for testing.
    
    Args:
        username: Username for the profile (default "pro_test_user")
        
    Returns:
        A new PerfilPro instance with default values
    """
    return PerfilPro(username=username, gemas=50, racha_dias=1, notificaciones_activas=True, meses_suscripcion=3)
