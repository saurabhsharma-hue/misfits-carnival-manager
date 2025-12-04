// Firebase Population Script for Misfits Carnival Manager
// Run this in the browser console at https://carnival.misfits.net.in

async function populateFirebaseWithSportsFever() {
    console.log('🎪 Starting Firebase population...');

    // Wait for Firebase to be ready
    while (!window.firebase) {
        console.log('Waiting for Firebase...');
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    console.log('✅ Firebase ready!');

    // Create Sports Fever carnival
    const sportsFever = {
        id: 1,
        name: "Sports Fever 2025",
        description: "Annual Sports Carnival featuring multiple sports activities",
        startDate: "2025-06-01",
        endDate: "2025-06-30"
    };

    // Create test club
    const testClub = {
        id: 1,
        name: "Delhi Football Club",
        activity: "Football",
        commissionType: "Percentage",
        commissionAmount: "5",
        carnivals: [1] // Sports Fever
    };

    // Mandatory template tasks (19 tasks)
    const mandatoryTasks = [
        { id: 1, description: "Once the leader reverts, event coordinator to sit with them, finalise the dates, event flow and commission %", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "high", progress: 0 },
        { id: 2, description: "Get the venue requested by the venue team and map a venue to the event", team: "Operations", owner: "Tauheed", status: "pending", createdAt: "2025-01-01", priority: "high", progress: 0 },
        { id: 3, description: "Prepare the content plan with marketing team - how much hype to be done, how etc etc and when", team: "Marketing", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 4, description: "Logistical requirement to be taken on a doc by the club and keep it somewhere against the club with the status of what all is done", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 5, description: "Banner to be created by the marketing team - alignment and completion", team: "Marketing", owner: "Ayushi", status: "pending", createdAt: "2025-01-01", priority: "high", progress: 0 },
        { id: 6, description: "Sharing event flow details with marketing team", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 7, description: "Logo to be created by the marketing team - alignment and completion", team: "Marketing", owner: "Ayushi", status: "pending", createdAt: "2025-01-01", priority: "high", progress: 0 },
        { id: 8, description: "Marketing asset requirement - Ideally I should be able to add under this section (Example - medals, certificate, standees)", team: "Marketing", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 9, description: "Banner to be placed in the festival section of the app", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 10, description: "Meetup creation and linking to the festival section", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 11, description: "Asset making by marketing team", team: "Marketing", owner: "Ayushi", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 12, description: "Asset printing", team: "Marketing", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "low", progress: 0 },
        { id: 13, description: "Asset delivery", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 14, description: "Logistical requirement delivery", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 15, description: "Logistical and asset implementation", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "high", progress: 0 },
        { id: 16, description: "Videographer requirement and alignment", team: "Marketing", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "low", progress: 0 },
        { id: 17, description: "Post event content", team: "Marketing", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "low", progress: 0 },
        { id: 18, description: "On ground assistant requirements", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 },
        { id: 19, description: "On ground assistant implementation", team: "Operations", owner: "Joy", status: "pending", createdAt: "2025-01-01", priority: "medium", progress: 0 }
    ];

    // Carnival-level tasks
    const carnivalTasks = [
        { description: "Deciding the fest name which is deciding the carnival name", team: "Operations", owner: "Joy", status: "pending", id: Date.now(), priority: "high" },
        { description: "Announcement to leaders group", team: "Operations", owner: "Joy", status: "pending", id: Date.now() + 1, priority: "medium" }
    ];

    try {
        console.log('📝 Saving carnivals...');
        await window.firebase.set(window.firebase.ref(window.firebase.database, 'carnivals'), [sportsFever]);

        console.log('🏢 Saving clubs...');
        await window.firebase.set(window.firebase.ref(window.firebase.database, 'clubs'), [testClub]);

        console.log('📋 Saving tasks...');
        const allTasksData = {
            1: { // Sports Fever carnival ID
                carnivalTasks: carnivalTasks,
                clubs: {
                    1: mandatoryTasks.map(task => ({
                        ...task,
                        clubId: 1,
                        carnivalId: 1,
                        id: task.id + 1000 // Ensure unique IDs
                    }))
                }
            }
        };

        await window.firebase.set(window.firebase.ref(window.firebase.database, 'tasks'), allTasksData);

        console.log('✅ Firebase population complete!');
        console.log('📊 Data populated:');
        console.log('   - 1 Carnival: Sports Fever 2025');
        console.log('   - 1 Club: Delhi Football Club');
        console.log('   - 2 Carnival Tasks');
        console.log('   - 19 Club Tasks (mandatory template)');
        console.log('   - Teams: Operations, Marketing, Finance');
        console.log('   - Owners: Joy, Ayushi, Tauheed');

        // Refresh the page to see the data
        alert('✅ Firebase populated successfully! Refreshing page to load data...');
        window.location.reload();

    } catch (error) {
        console.error('❌ Error populating Firebase:', error);
        alert('❌ Error: ' + error.message);
    }
}

// Run the population
populateFirebaseWithSportsFever();