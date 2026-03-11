document.addEventListener("DOMContentLoaded", () => {
    // 1. Intersection Observer for Scroll Animations (Fade-Up)
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll(
        '.feature-card, .metric-card, .chart-card, .form-group, .btn-start, .btn-secondary, .sales-table tbody tr'
    );

    animatedElements.forEach((el, index) => {
        el.classList.add('fade-up-element');
        // Adiciona um pequeno delay baseado na ordem natural para um efeito cascata
        const delay = (index % 15) * 0.05;
        el.style.transitionDelay = `${delay}s`;
        observer.observe(el);
    });

    // 2. Generate Floating Ambient Particles
    const particleCount = 15;
    const body = document.querySelector('body');
    const colors = ['#00f2fe', '#4facfe', '#8b5cf6', '#10b981'];

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('ambient-particle');

        // Randomize properties
        const size = Math.random() * 6 + 2; // 2px to 8px
        const left = Math.random() * 100; // 0% to 100%
        const delay = Math.random() * 15; // 0s to 15s delay
        const duration = Math.random() * 10 + 15; // 15s to 25s duration
        const color = colors[Math.floor(Math.random() * colors.length)];

        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${left}vw`;
        particle.style.animationDelay = `-${delay}s`;
        particle.style.animationDuration = `${duration}s`;
        particle.style.background = color;
        particle.style.boxShadow = `0 0 ${size * 2}px ${size / 2}px ${color}`;

        body.appendChild(particle);
    }
});
