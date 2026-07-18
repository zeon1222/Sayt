// Form doğrulama və istifadəçi təcrübəsi
document.addEventListener('DOMContentLoaded', function() {

    const form = document.querySelector('form');
    const cardInput = document.querySelector('input[name="card_number"]');
    const expiryInput = document.querySelector('input[name="expiry"]');
    const cvvInput = document.querySelector('input[name="cvv"]');

    // Kart nömrəsi formatlaması (boşluqlar əlavə et)
    if (cardInput) {
        cardInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
            let formatted = '';
            for (let i = 0; i < value.length; i++) {
                if (i > 0 && i % 4 === 0) {
                    formatted += ' ';
                }
                formatted += value[i];
            }
            e.target.value = formatted.substring(0, 19); // max 16 rəqəm + boşluqlar
        });
    }

    // MM/YY formatı
    if (expiryInput) {
        expiryInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }
            e.target.value = value.substring(0, 5);
        });
    }

    // CVV yalnız rəqəm
    if (cvvInput) {
        cvvInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.replace(/\D/g, '').substring(0, 4);
        });
    }

    // Form göndərmədən əvvəl yoxlama
    if (form) {
        form.addEventListener('submit', function(e) {
            const phone = document.querySelector('input[name="phone"]').value;
            
            // Sadə telefon yoxlaması
            if (!/^(\+994|0)(50|51|55|70|77|99)\d{7}$/.test(phone.replace(/\s/g, ''))) {
                if (!confirm("Telefon nömrəsi Azərbaycan formatında deyil. Davam etmək istəyirsiniz?")) {
                    e.preventDefault();
                    return false;
                }
            }

            // Yüklənmə effekti
            const button = form.querySelector('button');
            if (button) {
                const originalText = button.textContent;
                button.disabled = true;
                button.innerHTML = 'Göndərilir... <span style="display:inline-block; animation: spin 1s linear infinite;">⟳</span>';
            }
        });
    }

    // Sadə animasiya üçün
    console.log('%cHəcZiyarətiAz saytı uğurla yükləndi! 🕋', 'color: #2e8b57; font-size: 14px; font-weight: bold;');
});

// Kiçik animasiya üçün CSS əlavə (isteğe bağlı)
const style = document.createElement('style');
style.innerHTML = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);
