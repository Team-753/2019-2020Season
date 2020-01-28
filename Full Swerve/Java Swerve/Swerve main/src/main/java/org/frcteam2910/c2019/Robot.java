package org.frcteam2910.c2019;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.command.Scheduler;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.frcteam753.c2020.autonomous.AutonomousSelector;
import org.frcteam753.c2020.autonomous.AutonomousTrajectories;
import org.frcteam753.c2020.subsystems.*;
import org.frcteam753.c2020.vision.api.Gamepiece;
import org.frcteam753.common.robot.drivers.Limelight;
import org.frcteam753.common.robot.drivers.NavX;
import org.frcteam753.common.robot.subsystems.SubsystemManager;

public class Robot extends TimedRobot {
    private static final double UPDATE_DT = 5e-3; // 5 ms

    private final SubsystemManager subsystemManager = new SubsystemManager(
            
            DrivetrainSubsystem.getInstance(),
            
    );

    private static final OI oi = new OI();

    
    private AutonomousSelector autonomousSelector = new AutonomousSelector(autonomousTrajectories);

    private Command autonomousCommand = null;

    public Robot() {
       
    }

    public static OI getOi() {
        return oi;
    }

    @Override
    public void robotInit() {
        
        subsystemManager.enableKinematicLoop(UPDATE_DT);
    }

    @Override
    public void robotPeriodic() {
        
    }

    @Override
    public void teleopInit() {
//        if (autonomousCommand != null) {
//            autonomousCommand.cancel();
//            autonomousCommand = null;
//        }
    }

    @Override
    public void teleopPeriodic() {
        Scheduler.getInstance().run();
    }

    @Override
    public void autonomousInit() {
        if (autonomousCommand != null) {
            autonomousCommand.cancel();
        }

        autonomousCommand = autonomousSelector.getCommand();
        autonomousCommand.start();
    }

    @Override
    public void autonomousPeriodic() {
        Scheduler.getInstance().run();
    }

    @Override
    public void disabledInit() {
//        if (autonomousCommand != null) {
//            autonomousCommand.cancel();
//            autonomousCommand = null;
//        }
//        Scheduler.getInstance().removeAll();
    }

    @Override
    public void disabledPeriodic() {
        
    }
}
