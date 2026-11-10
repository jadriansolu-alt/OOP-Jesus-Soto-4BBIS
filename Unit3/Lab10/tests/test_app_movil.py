"""
Lab 10: Automated Testing with pytest - Test Suite for Mobile System Backend
Objet-Oriented Programming (OOP) Paradigm

This test suite validates the behavior of PerfilMovil and PerfilPro classes
through comprehensive automated unit testing using pytest framework.

Technical Criteria Implemented:
1. State Isolation (@pytest.fixture): Implementation of a fixture for provisioning 
   standardized instances of PerfilMovil.
2. Structural Integrity and Assertion Tests: Verification of initial attribute 
   assignment and arithmetic consistency in balance transactions.
3. Exception Validation (pytest.raises): Rigorous checking of error propagation 
   under invalid states or unauthorized transactions.
4. Parameterized Tests (@pytest.mark.parametrize): Efficient evaluation of multiple 
   test vectors for boundary inputs in the gem-earning methods.
5. Type and Hierarchy Verification (isinstance): Formal checking of the inheritance 
   relationship and the lifecycle of the PerfilPro subclass.
"""

import pytest
from app_movil import (
    PerfilMovil, 
    PerfilPro, 
    SuscripcionExpiradaError, 
    PuntosInsuficientesError,
    create_standard_profile,
    create_standard_pro_profile
)


# ============================================================================
# 1. STATE ISOLATION (@pytest.fixture)
# Implementation of a fixture for provisioning standardized instances of PerfilMovil.
# ============================================================================

@pytest.fixture
def standard_movil_profile():
    """
    Fixture that creates and returns a standardized PerfilMovil instance for testing.
    
    This ensures each test starts with a clean, predictable state.
    Default values: username="test_user", gemas=50, racha_dias=1, notificaciones_activas=True
    """
    return create_standard_profile(username="test_user")


@pytest.fixture
def standard_pro_profile():
    """
    Fixture that creates and returns a standardized PerfilPro instance for testing.
    
    Default values: username="pro_test_user", gemas=50, racha_dias=1, 
                    notificaciones_activas=True, meses_suscripcion=3
    """
    return create_standard_pro_profile(username="pro_test_user")


# ============================================================================
# 2. STRUCTURAL INTEGRITY AND ASSERTION TESTS
# Verification of initial attribute assignment and arithmetic consistency in balance transactions.
# ============================================================================

class TestPerfilMovil_InitialState:
    """Tests for PerfilMovil initial state validation."""
    
    def test_initial_attributes_default_values(self, standard_movil_profile):
        """Test that default values are correctly set on initialization."""
        profile = standard_movil_profile
        
        # Verify gemas starts at 50
        assert profile.gemas == 50, "Initial gemas should be 50"
        
        # Verify racha_dias starts at 1
        assert profile.racha_dias == 1, "Initial racha_dias should be 1"
        
        # Verify notificaciones_activas defaults to True
        assert profile.notificaciones_activas is True, "Default notificaciones_activas should be True"
    
    def test_initial_attributes_custom_values(self):
        """Test that custom initial values are correctly set."""
        profile = PerfilMovil(
            username="custom_user",
            gemas=100,
            racha_dias=5,
            notificaciones_activas=False
        )
        
        assert profile.username == "custom_user"
        assert profile.gemas == 100
        assert profile.racha_dias == 5
        assert profile.notificaciones_activas is False
    
    def test_initial_gemas_negative_raises_valueerror(self):
        """Test that negative initial gemas raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            PerfilMovil(username="test", gemas=-10)
        
        assert "negativo" in str(exc_info.value).lower()


class TestPerfilMovil_GemasOperations:
    """Tests for gem balance arithmetic operations."""
    
    def test_ganar_gemas_increments_balance(self, standard_movil_profile):
        """Test that ganar_gemas correctly increments the balance."""
        profile = standard_movil_profile
        
        initial_gemas = profile.gemas
        amount_to_win = 25
        
        # Execute operation
        new_balance = profile.ganar_gemas(amount_to_win)
        
        # Verify new balance
        assert new_balance == initial_gemas + amount_to_win, \
            f"Expected {initial_gemas + amount_to_win}, got {new_balance}"
        assert profile.gemas == new_balance
    
    def test_gastar_gemas_decrements_balance(self, standard_movil_profile):
        """Test that gastar_gemas correctly decrements the balance."""
        profile = standard_movil_profile
        
        initial_gemas = profile.gemas
        amount_to_spend = 20
        
        # Execute operation
        new_balance = profile.gastar_gemas(amount_to_spend)
        
        # Verify new balance
        assert new_balance == initial_gemas - amount_to_spend, \
            f"Expected {initial_gemas - amount_to_spend}, got {new_balance}"
        assert profile.gemas == new_balance
    
    def test_multiple_gem_transactions(self):
        """Test multiple sequential gem transactions."""
        profile = PerfilMovil(username="multi_test", gemas=100)
        
        # Win 50 gems
        profile.ganar_gemas(50)
        assert profile.gemas == 150
        
        # Spend 30 gems
        profile.gastar_gemas(30)
        assert profile.gemas == 120
        
        # Win 25 more gems
        profile.ganar_gemas(25)
        assert profile.gemas == 145
        
        # Spend 75 gems (should work since we have 145)
        profile.gastar_gemas(75)
        assert profile.gemas == 70


# ============================================================================
# 3. EXCEPTION VALIDATION (pytest.raises)
# Rigorous checking of error propagation under invalid states or unauthorized transactions.
# ============================================================================

class TestPerfilMovil_Exceptions:
    """Tests for exception handling in PerfilMovil."""
    
    def test_ganar_gemas_negative_raises_valueerror(self, standard_movil_profile):
        """Test that ganar_gemas with negative amount raises ValueError."""
        profile = standard_movil_profile
        
        with pytest.raises(ValueError) as exc_info:
            profile.ganar_gemas(-10)
        
        assert "positiva" in str(exc_info.value).lower()
    
    def test_ganar_gemas_zero_raises_valueerror(self, standard_movil_profile):
        """Test that ganar_gemas with zero amount raises ValueError."""
        profile = standard_movil_profile
        
        with pytest.raises(ValueError) as exc_info:
            profile.ganar_gemas(0)
        
        assert "positiva" in str(exc_info.value).lower()
    
    def test_gastar_gemas_negative_raises_valueerror(self, standard_movil_profile):
        """Test that gastar_gemas with negative amount raises ValueError."""
        profile = standard_movil_profile
        
        with pytest.raises(ValueError) as exc_info:
            profile.gastar_gemas(-10)
        
        assert "positiva" in str(exc_info.value).lower()
    
    def test_gastar_gemas_zero_raises_valueerror(self, standard_movil_profile):
        """Test that gastar_gemas with zero amount raises ValueError."""
        profile = standard_movil_profile
        
        with pytest.raises(ValueError) as exc_info:
            profile.gastar_gemas(0)
        
        assert "positiva" in str(exc_info.value).lower()
    
    def test_gastar_gemas_insufficient_funds_raises_puntosinsuficienteserror(self, standard_movil_profile):
        """Test that gastar_gemas with insufficient funds raises PuntosInsuficientesError."""
        profile = standard_movil_profile  # Starts with 50 gems
        
        with pytest.raises(PuntosInsuficientesError) as exc_info:
            profile.gastar_gemas(100)  # Try to spend more than available
        
        assert "insuficientes" in str(exc_info.value).lower()
        assert exc_info.value.required == 100
        assert exc_info.value.available == 50
    
    def test_exact_amount_spend_works(self, standard_movil_profile):
        """Test that spending exact amount works correctly."""
        profile = standard_movil_profile
        
        # Should be able to spend exactly what we have (50 gems)
        new_balance = profile.gastar_gemas(50)
        
        assert new_balance == 0
        assert profile.gemas == 0
    
    def test_spend_more_than_exact_amount_raises_error(self, standard_movil_profile):
        """Test that spending more than exact amount raises error."""
        profile = standard_movil_profile
        
        with pytest.raises(PuntosInsuficientesError) as exc_info:
            profile.gastar_gemas(51)  # Try to spend 1 more than available
        
        assert "insuficientes" in str(exc_info.value).lower()


# ============================================================================
# 4. PARAMETERIZED TESTS (@pytest.mark.parametrize)
# Efficient evaluation of multiple test vectors for boundary inputs in the gem-earning methods.
# ============================================================================

class TestPerfilMovil_Parameterized:
    """Parameterized tests for various input scenarios."""
    
    @pytest.mark.parametrize("username,initial_gemas,racha_dias,notificaciones", [
        ("user1", 50, 1, True),
        ("user2", 100, 5, False),
        ("user3", 200, 10, True),
        ("user4", 75, 3, True),
    ])
    def test_multiple_user_initializations(self, username, initial_gemas, racha_dias, notificaciones):
        """Test initialization with various parameter combinations."""
        profile = PerfilMovil(
            username=username,
            gemas=initial_gemas,
            racha_dias=racha_dias,
            notificaciones_activas=notificaciones
        )
        
        assert profile.username == username
        assert profile.gemas == initial_gemas
        assert profile.racha_dias == racha_dias
        assert profile.notificaciones_activas is notificaciones
    
    @pytest.mark.parametrize("username,gem_amount", [
        ("winner1", 25),
        ("winner2", 50),
        ("winner3", 100),
        ("winner4", 200),
    ])
    def test_ganar_gemas_with_various_amounts(self, username, gem_amount):
        """Test ganar_gemas with various positive amounts."""
        profile = PerfilMovil(username=username)
        
        initial_balance = profile.gemas
        new_balance = profile.ganar_gemas(gem_amount)
        
        assert new_balance == initial_balance + gem_amount
    
    @pytest.mark.parametrize("username,spend_amount", [
        ("spender1", 10),
        ("spender2", 30),
        ("spender3", 50),
        ("spender4", 40),
    ])
    def test_gastar_gemas_with_various_amounts(self, username, spend_amount):
        """Test gastar_gemas with various amounts that should succeed."""
        profile = PerfilMovil(username=username, gemas=100)  # Start with 100 gems
        
        initial_balance = profile.gemas
        new_balance = profile.gastar_gemas(spend_amount)
        
        assert new_balance == initial_balance - spend_amount


# ============================================================================
# 5. TYPE AND HIERARCHY VERIFICATION (isinstance)
# Formal checking of the inheritance relationship and the lifecycle of the PerfilPro subclass.
# ============================================================================

class TestPerfilPro_Inheritance:
    """Tests for PerfilPro inheritance from PerfilMovil."""
    
    def test_perfilpro_is_instance_of_perfilmovil(self):
        """Test that PerfilPro is an instance of PerfilMovil (inheritance check)."""
        pro_profile = PerfilPro(username="pro_user")
        
        # Verify isinstance relationship
        assert isinstance(pro_profile, PerfilPro), "Should be instance of PerfilPro"
        assert isinstance(pro_profile, PerfilMovil), "Should also be instance of PerfilMovil (inheritance)"
    
    def test_perfilpro_has_additional_attributes(self):
        """Test that PerfilPro has additional attributes beyond base class."""
        pro_profile = PerfilPro(username="pro_user", meses_suscripcion=3)
        
        # Check inherited attributes
        assert hasattr(pro_profile, 'username')
        assert hasattr(pro_profile, 'gemas')
        assert hasattr(pro_profile, 'racha_dias')
        assert hasattr(pro_profile, 'notificaciones_activas')
        
        # Check additional PRO-specific attributes
        assert hasattr(pro_profile, 'meses_suscripcion'), "Should have meses_suscripcion attribute"
        assert pro_profile.meses_suscripcion == 3
        
        # Check es_pro attribute (should be True by default)
        assert hasattr(pro_profile, 'es_pro')
        assert pro_profile.es_pro is True
    
    def test_perfilpro_inherits_methods(self):
        """Test that PerfilPro inherits methods from PerfilMovil."""
        pro_profile = PerfilPro(username="pro_user")
        
        # Verify inherited methods exist and work
        assert hasattr(pro_profile, 'ganar_gemas')
        assert hasattr(pro_profile, 'gastar_gemas')
        
        # Test that inherited methods work correctly
        initial_gemas = pro_profile.gemas
        pro_profile.ganar_gemas(25)
        assert pro_profile.gemas == 75
        
        pro_profile.gastar_gemas(10)
        assert pro_profile.gemas == 65


class TestPerfilPro_Lifecycle:
    """Tests for PerfilPro lifecycle and state transitions."""
    
    def test_perfilpro_initialization_with_custom_values(self):
        """Test PerfilPro initialization with custom values."""
        profile = PerfilPro(
            username="custom_pro",
            gemas=200,
            racha_dias=10,
            notificaciones_activas=True,
            meses_suscripcion=6
        )
        
        assert profile.username == "custom_pro"
        assert profile.gemas == 200
        assert profile.racha_dias == 10
        assert profile.notificaciones_activas is True
        assert profile.meses_suscripcion == 6
        assert profile.es_pro is True
    
    def test_perfilpro_negative_meses_suscripcion_raises_valueerror(self):
        """Test that negative meses_suscripcion raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            PerfilPro(username="test", meses_suscripcion=-1)
        
        assert "mayor a cero" in str(exc_info.value).lower() or "greater than zero" in str(exc_info.value).lower()
    
    def test_perfilpro_zero_meses_suscripcion_raises_valueerror(self):
        """Test that zero meses_suscripcion raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            PerfilPro(username="test", meses_suscripcion=0)
        
        assert "mayor a cero" in str(exc_info.value).lower() or "greater than zero" in str(exc_info.value).lower()


class TestPerfilPro_SpecializedMethod:
    """Tests for the specialized descargar_contenido_offline method."""
    
    def test_descargar_contenido_offline_success(self, standard_pro_profile):
        """Test successful content download when subscription is active."""
        profile = standard_pro_profile  # meses_suscripcion=3
        
        result = profile.descargar_contenido_offline()
        
        assert "Descarga exitosa" in result
        assert "PRO activa" in result
        assert "meses restantes" in result
    
    def test_descargar_contenido_offline_expired_subscription(self):
        """Test content download when subscription has expired."""
        # Create a profile with 1 month, then manually expire it for testing
        profile = PerfilPro(
            username="expired_user",
            gemas=50,
            racha_dias=1,
            notificaciones_activas=True,
            meses_suscripcion=1  # Start active
        )
        
        # Manually expire the subscription for testing purposes
        profile.meses_suscripcion = 0
        
        with pytest.raises(SuscripcionExpiradaError) as exc_info:
            profile.descargar_contenido_offline()
        
        error_msg = str(exc_info.value)
        assert "expirado" in error_msg.lower() or "expired" in error_msg.lower()
    
    def test_descargar_contenido_offline_switches_state_on_expiration(self):
        """Test that expired subscription switches es_pro to False."""
        # Create a profile with 1 month, then expire it
        profile = PerfilPro(
            username="expiring_user",
            gemas=50,
            racha_dias=1,
            notificaciones_activas=True,
            meses_suscripcion=1
        )
        
        # First call should succeed
        result1 = profile.descargar_contenido_offline()
        assert "Descarga exitosa" in result1
        
        # Manually expire the subscription
        profile.meses_suscripcion = 0
        
        # Second call should raise exception and switch state
        with pytest.raises(SuscripcionExpiradaError):
            profile.descargar_contenido_offline()
        
        assert profile.es_pro is False, "es_pro should be switched to False on expiration"


# ============================================================================
# 6. INTEGRATION TESTS - Combining Multiple Scenarios
# ============================================================================

class TestIntegrationScenarios:
    """Integration tests that combine multiple operations and states."""
    
    def test_full_gem_lifecycle(self):
        """Test a complete gem earning/spending lifecycle."""
        profile = PerfilMovil(username="lifecycle_test", gemas=50)
        
        # Initial state
        assert profile.gemas == 50
        
        # Win some gems
        profile.ganar_gemas(100)
        assert profile.gemas == 150
        
        # Spend some gems
        profile.gastar_gemas(75)
        assert profile.gemas == 75
        
        # Win more
        profile.ganar_gemas(25)
        assert profile.gemas == 100
        
        # Final spend that leaves us with minimal gems
        profile.gastar_gemas(75)
        assert profile.gemas == 25
    
    def test_pro_subscription_lifecycle(self):
        """Test a complete PRO subscription lifecycle."""
        profile = PerfilPro(username="pro_lifecycle", gemas=50, meses_suscripcion=3)
        
        # Active subscription
        assert profile.es_pro is True
        assert profile.meses_suscripcion == 3
        
        # Successful download
        result = profile.descargar_contenido_offline()
        assert "Descarga exitosa" in result
        
        # Manually expire the subscription
        profile.meses_suscripcion = 0
        
        # Now should raise exception and switch state
        with pytest.raises(SuscripcionExpiradaError):
            profile.descargar_contenido_offline()
        
        assert profile.es_pro is False


# ============================================================================
# 7. BOUNDARY AND EDGE CASE TESTS
# ============================================================================

class TestBoundaryConditions:
    """Tests for boundary and edge case conditions."""
    
    def test_ganar_gemas_with_very_small_amount(self, standard_movil_profile):
        """Test ganar_gemas with very small positive amount (boundary)."""
        profile = standard_movil_profile
        
        # Should work with 0.01 if we were using floats, but we use ints
        new_balance = profile.ganar_gemas(1)  # Minimum integer
        assert new_balance == 51
    
    def test_gastar_gemas_with_exact_remaining_amount(self):
        """Test gastar_gemas with exact remaining amount."""
        profile = PerfilMovil(username="exact_test", gemas=25)
        
        # Should be able to spend exactly what we have
        new_balance = profile.gastar_gemas(25)
        assert new_balance == 0
    
    def test_username_with_special_characters(self):
        """Test username validation with special characters."""
        profile = PerfilMovil(username="user_123_test")
        assert profile.username == "user_123_test"
        
        # Test that whitespace is stripped
        profile2 = PerfilMovil(username="  trimmed_user  ")
        assert profile2.username == "trimmed_user"


# ============================================================================
# 8. RUN THE TEST SUITE
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("LAB 10: AUTOMATED TESTING WITH PYTEST - TEST SUITE")
    print("=" * 80)
    
    # Run all tests with verbose output
    pytest.main([__file__, "-v"])