import React from 'react';
import { motion } from 'framer-motion';

const QuestionCard = ({ question, questionIndex, totalQuestions, selectedAnswer, onAnswer }) => {
    return (
        <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="bg-white rounded-xl shadow-lg p-6 max-w-2xl w-full"
        >
            <div className="flex justify-between items-center mb-4">
                <span className="text-sm font-medium text-gray-500">Question {questionIndex + 1} of {totalQuestions}</span>
            </div>

            <h3 className="text-xl font-semibold text-gray-800 mb-6">{question.question}</h3>

            <div className="space-y-3">
                {Object.entries(question.options).map(([key, value]) => (
                    <button
                        key={key}
                        onClick={() => onAnswer(key)}
                        className={`w-full text-left p-4 rounded-lg border-2 transition-all ${selectedAnswer === key
                                ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                                : 'border-gray-200 hover:border-indigo-300 hover:bg-gray-50'
                            }`}
                    >
                        <span className="font-bold mr-2 uppercase">{key})</span> {value}
                    </button>
                ))}
            </div>
        </motion.div>
    );
};

export default QuestionCard;
