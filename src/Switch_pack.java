package Test;

import java.io.IOException;

import android.os.Bundle;
import android.os.RemoteException;

import com.android.uiautomator.core.UiDevice;
import com.android.uiautomator.core.UiObject;
import com.android.uiautomator.core.UiObjectNotFoundException;
import com.android.uiautomator.core.UiSelector;
import com.android.uiautomator.testrunner.UiAutomatorTestCase;
import com.android.uiautomator.core.UiWatcher;
import com.android.uiautomator.core.UiScrollable;

public class Switch_pack extends UiAutomatorTestCase {

	
	
	public void Switch_package() throws UiObjectNotFoundException, RemoteException, Exception{
		
		int x =UiDevice.getInstance().getDisplayWidth();
		int y =UiDevice.getInstance().getDisplayHeight();
		
		Bundle bundle = getParams();
		String switch_package =bundle.getString("package");
		
		if (switch_package.contains("-"))
		{
			switch_package = switch_package.replace("-", " - ");
		}
		
		System.out.print(switch_package);
		try {
			UiDevice.getInstance().wakeUp();
		} catch (RemoteException e) {
		// TODO Auto-generated catch block
		e.printStackTrace();
		}
		UiDevice.getInstance().swipe(x/2, y/10*9, x/2, y/10, 30);
		
		sleep(2000);
		UiObject welcome = new UiObject(new UiSelector().text("GOT IT"));
		if (welcome.exists()){
			welcome.click();
			sleep(2000);
		}
		UiDevice.getInstance().pressHome();
		
		Runtime.getRuntime().exec("am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n com.qualcomm.qti.carrierconfigure/.ConfigurationActivity");
		sleep(2000);

		for (int i=0;i<30;i++){
			UiDevice.getInstance().swipe(x/2,y/5*3,x/2,y/5*4,20);
			sleep(500);
		}
		UiObject package_name = new UiObject(new UiSelector().textContains(switch_package));
		UiObject aceptar = new UiObject(new UiSelector().resourceId("android:id/button1"));
		if (switch_package.equals("Default"))
		{
			UiObject first_choose = new UiObject(new UiSelector().resourceId("com.qualcomm.qti.carrierconfigure:id/radio_button"));
			first_choose.click();
			sleep(2000);
	    	aceptar.click();
		}
		else{
			 for(int i=0;i<15;i++)
			    {
				    if (package_name.exists())
				    {
				    	package_name.click();
				    	sleep(2000);
				    	aceptar.click();
				    	break;
				    }
				    else
				    {
				    	UiDevice.getInstance().swipe(x/2,y/5*4,x/2,y/5*2,20);
				    	sleep(2000);
				    }
			    }
				
		}
	   
	}
	
}
