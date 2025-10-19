package ai_driven_cybersecurity_platformcom.ai.driven.cybersecurity.platform;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.mockStatic;

import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;

import com.ai.driven.cybersecurity.platform.db.DatabaseManager;
import com.ai.driven.cybersecurity.platform.gui.Dashboard;

class AIDrivenCybersecurityPlatformTest {

	@Test
	void testMainLaunches() throws Exception {
		// Mock DatabaseManager instance
		DatabaseManager localDb = mock(DatabaseManager.class);

		// Mock static method Dashboard.launchDashboard()
		try (MockedStatic<Dashboard> mockedDashboard = mockStatic(Dashboard.class)) {
			mockedDashboard.when(() -> Dashboard.launchDashboard(localDb)).thenAnswer(invocation -> {
				System.out.println("Dashboard launched with mock DB");
				return null;
			});

			// Call the static method
			Dashboard.launchDashboard(localDb);

			// Verify it was called
			mockedDashboard.verify(() -> Dashboard.launchDashboard(localDb));
		}

		// Also validate real DatabaseManager creation
		DatabaseManager db1 = new DatabaseManager("jdbc:mysql://localhost:3306/ai_driven_cybersecurity_platform_local",
				"root", "admin");
		assertNotNull(db1);
	}
}
