// Debug script to inject into main app console
// Copy and paste this entire script into the browser console when main app is loaded

console.log('🔧 INJECTING TIMELINE DEBUG TOOLS');

// Override the original function with debug version
window.originalUpdateTimelineDropdowns = window.updateTimelineDropdowns;

window.updateTimelineDropdowns = function() {
    console.log('🔄 INTERCEPTED updateTimelineDropdowns call');

    try {
        // Check if data exists
        console.log('📋 Data check:');
        console.log('  - carnivalsList:', typeof carnivalsList, carnivalsList?.length);
        console.log('  - clubsList:', typeof clubsList, clubsList?.length);
        console.log('  - allTasks:', typeof allTasks, Object.keys(allTasks || {}));

        // Check if elements exist
        console.log('🔍 Element check:');
        const elements = [
            'timeline-carnival-filter',
            'timeline-club-filter',
            'timeline-team-filter',
            'timeline-owner-filter',
            'timeline-status-filter'
        ];

        let allElementsFound = true;
        elements.forEach(id => {
            const el = document.getElementById(id);
            console.log(`  - ${id}:`, el ? 'EXISTS' : 'NOT FOUND');
            if (!el) allElementsFound = false;
        });

        if (!allElementsFound) {
            console.error('❌ Some dropdown elements missing!');
            return;
        }

        // Call original function
        console.log('✅ Calling original updateTimelineDropdowns...');
        return window.originalUpdateTimelineDropdowns();

    } catch (error) {
        console.error('❌ Error in debug wrapper:', error);
        console.error('Stack:', error.stack);
    }
};

// Function to manually trigger timeline rendering
window.debugRenderTimeline = function() {
    console.log('🔧 Manual timeline render...');
    try {
        renderTimeline();
    } catch (error) {
        console.error('❌ Error in renderTimeline:', error);
    }
};

// Function to check current view
window.debugCurrentView = function() {
    console.log('🔍 Current view check:');
    const views = ['dashboard', 'task-tracker', 'timeline', 'setup'];
    views.forEach(view => {
        const el = document.getElementById(view + '-view');
        if (el) {
            const isHidden = el.classList.contains('hidden');
            console.log(`  - ${view}: ${isHidden ? 'HIDDEN' : 'VISIBLE'}`);
        }
    });
};

// Function to force show timeline
window.debugShowTimeline = function() {
    console.log('🔧 Forcing timeline view...');
    try {
        showView('timeline');
    } catch (error) {
        console.error('❌ Error showing timeline:', error);
    }
};

// Check for JavaScript errors
window.addEventListener('error', function(e) {
    console.error('🚨 JavaScript Error:', e.error);
    console.error('File:', e.filename, 'Line:', e.lineno);
});

console.log('✅ Debug tools loaded. Available commands:');
console.log('- debugCurrentView() - Check which view is active');
console.log('- debugShowTimeline() - Force show timeline view');
console.log('- debugRenderTimeline() - Manually trigger timeline render');
console.log('- updateTimelineDropdowns() - Test dropdown population');

// Auto-check current state
debugCurrentView();