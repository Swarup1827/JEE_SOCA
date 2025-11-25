import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import QuestionCard from '../components/QuestionCard';

const CORE_SUBJECTS = ["Physics", "Chemistry", "Mathematics"];
const TIMER_DURATION = 30 * 60; // 30 minutes in seconds

const Test = () => {
    const navigate = useNavigate();
    const [subjects, setSubjects] = useState([]);
    const [currentSubjectIndex, setCurrentSubjectIndex] = useState(0);
    const [questions, setQuestions] = useState({});
    const [answers, setAnswers] = useState({});
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

    // New State for Features
    const [timeLeft, setTimeLeft] = useState(TIMER_DURATION);
    const [showTransition, setShowTransition] = useState(false);
    const [isTimerActive, setIsTimerActive] = useState(true);

    useEffect(() => {
        fetchSubjects();
    }, []);

    // Timer Logic
    useEffect(() => {
        let interval;
        if (isTimerActive && timeLeft > 0) {
            interval = setInterval(() => {
                setTimeLeft((prev) => {
                    if (prev <= 1) {
                        handleTimerExpiry();
                        return 0;
                    }
                    return prev - 1;
                });
            }, 1000);
        }
        return () => clearInterval(interval);
    }, [isTimerActive, timeLeft]);

    const handleTimerExpiry = () => {
        setIsTimerActive(false);
        alert("Time's up for the core subjects! Moving to the next section.");
        // Find index of first non-core subject (Well-being)
        const firstNonCoreIndex = subjects.findIndex(s => !CORE_SUBJECTS.includes(s));
        if (firstNonCoreIndex !== -1) {
            setShowTransition(true);
            setCurrentSubjectIndex(firstNonCoreIndex);
            setCurrentQuestionIndex(0);
            fetchQuestions(subjects[firstNonCoreIndex]);
        } else {
            handleSubmit();
        }
    };

    const formatTime = (seconds) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    };

    const fetchSubjects = async () => {
        try {
            const response = await axios.get('/api/subjects');
            setSubjects(response.data.subjects);
            // Fetch questions for the first subject
            if (response.data.subjects.length > 0) {
                fetchQuestions(response.data.subjects[0]);
            }
        } catch (error) {
            console.error('Error fetching subjects:', error);
            setLoading(false);
        }
    };

    const fetchQuestions = async (subject) => {
        if (questions[subject]) {
            setLoading(false);
            return;
        }

        setLoading(true);
        try {
            const response = await axios.get(`/api/questions/${subject}`);
            setQuestions(prev => ({
                ...prev,
                [subject]: response.data.questions
            }));
        } catch (error) {
            console.error(`Error fetching questions for ${subject}:`, error);
        } finally {
            setLoading(false);
        }
    };

    const handleAnswer = (answer) => {
        const currentSubject = subjects[currentSubjectIndex];
        // Store answer with Q-index format expected by backend (Q1, Q2...)
        // Note: backend expects 1-based index
        const questionKey = `Q${currentQuestionIndex + 1}`;

        setAnswers(prev => ({
            ...prev,
            [currentSubject]: {
                ...(prev[currentSubject] || {}),
                [questionKey]: answer
            }
        }));
    };

    const handleNext = async () => {
        const currentSubject = subjects[currentSubjectIndex];
        const subjectQuestions = questions[currentSubject] || [];

        if (currentQuestionIndex < subjectQuestions.length - 1) {
            setCurrentQuestionIndex(prev => prev + 1);
        } else {
            // Move to next subject
            if (currentSubjectIndex < subjects.length - 1) {
                const nextSubject = subjects[currentSubjectIndex + 1];

                // Check if we are moving from Core to Non-Core
                const isCurrentCore = CORE_SUBJECTS.includes(currentSubject);
                const isNextCore = CORE_SUBJECTS.includes(nextSubject);

                if (isCurrentCore && !isNextCore) {
                    setIsTimerActive(false); // Stop timer
                    setShowTransition(true);
                    setCurrentSubjectIndex(prev => prev + 1);
                    setCurrentQuestionIndex(0);
                    await fetchQuestions(nextSubject);
                } else {
                    setCurrentSubjectIndex(prev => prev + 1);
                    setCurrentQuestionIndex(0);
                    await fetchQuestions(nextSubject);
                }
            } else {
                // Submit test
                handleSubmit();
            }
        }
    };

    const handlePrev = () => {
        if (currentQuestionIndex > 0) {
            setCurrentQuestionIndex(prev => prev - 1);
        } else if (currentSubjectIndex > 0) {
            const prevSubject = subjects[currentSubjectIndex - 1];
            // Prevent going back to Core from Non-Core if timer expired/transition happened?
            // For simplicity, allow it but timer logic might get tricky.
            // Let's keep it simple: if we go back to core, timer resumes?
            // Actually, standard tests don't usually allow going back to timed sections once submitted.
            // But let's allow basic navigation for now.

            setCurrentSubjectIndex(prev => prev - 1);
            setCurrentQuestionIndex((questions[prevSubject]?.length || 1) - 1);
        }
    };

    const handleSubmit = async () => {
        setSubmitting(true);
        try {
            const response = await axios.post('/api/analyze', { user_answers: answers });
            // Navigate to analysis page with results
            navigate('/analysis', { state: { results: response.data.analysis } });
        } catch (error) {
            console.error('Error submitting test:', error);
            alert('Failed to submit test. Please try again.');
        } finally {
            setSubmitting(false);
        }
    };

    const startNonCoreSection = () => {
        setShowTransition(false);
    };

    if (loading && !questions[subjects[currentSubjectIndex]]) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-50">
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-indigo-600"></div>
            </div>
        );
    }

    if (submitting) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
                <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-indigo-600 mb-4"></div>
                <h2 className="text-xl font-semibold text-gray-700">Analyzing your performance...</h2>
                <p className="text-gray-500">Using Google Gemini AI for deep insights...</p>
            </div>
        );
    }

    // Transition Screen
    if (showTransition) {
        return (
            <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 text-white p-4">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 max-w-2xl text-center shadow-2xl"
                >
                    <h1 className="text-4xl font-bold mb-6">Great Job! 🎉</h1>
                    <p className="text-xl mb-8">
                        You've completed the core academic subjects. Now, let's take a moment to reflect on your well-being and study habits.
                    </p>
                    <div className="bg-white/20 rounded-xl p-6 mb-8 text-left">
                        <h3 className="text-lg font-semibold mb-4">Next Section:</h3>
                        <ul className="space-y-2">
                            <li className="flex items-center">🧘 Well-being Assessment</li>
                            <li className="flex items-center">⏰ Time Management Check</li>
                        </ul>
                    </div>
                    <button
                        onClick={startNonCoreSection}
                        className="bg-white text-indigo-600 px-8 py-3 rounded-full font-bold text-lg shadow-lg hover:bg-indigo-50 transition-colors"
                    >
                        Continue to Well-being Section
                    </button>
                </motion.div>
            </div>
        );
    }

    const currentSubject = subjects[currentSubjectIndex];
    const currentQuestions = questions[currentSubject] || [];
    const currentQuestion = currentQuestions[currentQuestionIndex];
    const currentAnswer = answers[currentSubject]?.[`Q${currentQuestionIndex + 1}`];
    const isCore = CORE_SUBJECTS.includes(currentSubject);

    return (
        <div className="min-h-screen bg-gray-50 py-8 px-4 flex flex-col items-center">
            {/* Header with Timer */}
            <div className="w-full max-w-4xl flex justify-between items-center mb-6 bg-white p-4 rounded-xl shadow-sm">
                <div>
                    <h2 className="text-lg font-bold text-gray-800">{currentSubject}</h2>
                    <p className="text-sm text-gray-500">Subject {currentSubjectIndex + 1} of {subjects.length}</p>
                </div>

                {isCore && (
                    <div className={`flex items-center px-4 py-2 rounded-lg font-mono font-bold text-xl ${timeLeft < 300 ? 'bg-red-100 text-red-600' : 'bg-indigo-50 text-indigo-600'
                        }`}>
                        ⏰ {formatTime(timeLeft)}
                    </div>
                )}
            </div>

            {/* Progress Bar */}
            <div className="w-full max-w-2xl mb-8">
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-indigo-600 transition-all duration-500"
                        style={{ width: `${((currentSubjectIndex) / subjects.length) * 100}%` }}
                    />
                </div>
            </div>

            <AnimatePresence mode='wait'>
                {currentQuestion && (
                    <QuestionCard
                        key={`${currentSubject}-${currentQuestionIndex}`}
                        question={currentQuestion}
                        questionIndex={currentQuestionIndex}
                        totalQuestions={currentQuestions.length}
                        selectedAnswer={currentAnswer}
                        onAnswer={handleAnswer}
                    />
                )}
            </AnimatePresence>

            <div className="flex justify-between w-full max-w-2xl mt-8">
                <button
                    onClick={handlePrev}
                    disabled={currentSubjectIndex === 0 && currentQuestionIndex === 0}
                    className={`px-6 py-2 rounded-lg font-medium transition-colors ${currentSubjectIndex === 0 && currentQuestionIndex === 0
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                        }`}
                >
                    Previous
                </button>

                <button
                    onClick={handleNext}
                    disabled={!currentAnswer}
                    className={`px-6 py-2 rounded-lg font-medium transition-colors ${!currentAnswer
                        ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                        : 'bg-indigo-600 text-white hover:bg-indigo-700 shadow-md'
                        }`}
                >
                    {currentSubjectIndex === subjects.length - 1 && currentQuestionIndex === currentQuestions.length - 1
                        ? 'Submit Test'
                        : 'Next'}
                </button>
            </div>
        </div>
    );
};

export default Test;
