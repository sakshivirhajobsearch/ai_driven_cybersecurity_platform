package ai_driven_cybersecurity_platformcom.ai.driven.cybersecurity.platform;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.mockStatic;

import org.junit.jupiter.api.Test;
import org.mockito.MockedStatic;

import com.ai.driven.cybersecurity.platform.db.DatabaseManager;
import com.ai.driven.cybersecurity.platform.gui.Dashboard;

class DashboardTest {

	@Test
	void testLaunchDashboardStatic() {
		DatabaseManager mockDb = mock(DatabaseManager.class);

		try (MockedStatic<Dashboard> mocked = mockStatic(Dashboard.class)) {
			mocked.when(() -> Dashboard.launchDashboard(mockDb)).thenAnswer(invocation -> {
				System.out.println("Dashboard launched with mock DB");
				return null;
			});

			// Call the static method
			Dashboard.launchDashboard(mockDb);

			// Verify it was called
			mocked.verify(() -> Dashboard.launchDashboard(mockDb));
		}
	}
}
