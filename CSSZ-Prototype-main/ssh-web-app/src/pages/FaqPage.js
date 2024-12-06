import React from 'react';

const FaqPage = () => {
    const faqs = [
        {
            question: "What is SSH Smart Homes?",
            answer: "SSH Smart Homes is a smart home system designed to enhance student living by offering tailored recipe recommendations and inventory tracking."
        },
        {
            question: "How does the SSH Camera work?",
            answer: "The SSH Camera uses image recognition to track inventory and expiration dates in your fridge, helping reduce food waste and streamline meal planning."
        },
        {
            question: "Can I customize my dietary preferences?",
            answer: "Yes, SSH allows you to set up a dietary profile for personalized recipe suggestions based on your needs."
        },
        {
            question: "How do I register for SSH?",
            answer: "You can register by navigating to the 'Register' page and filling out the required information."
        },
        {
            question: "What platforms support SSH Smart Homes?",
            answer: "SSH Smart Homes is accessible via web browsers on desktops, tablets, and mobile devices."
        }
    ];

    return (
        <div className="container-fluid mainContainer">
            <h1 className="title_features">Frequently Asked Questions</h1>
            <div className="faq-section">
                {faqs.map((faq, index) => (
                    <div key={index} className="faq-item">
                        <h2 className="subHeading_style">{faq.question}</h2>
                        <p>{faq.answer}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default FaqPage;
