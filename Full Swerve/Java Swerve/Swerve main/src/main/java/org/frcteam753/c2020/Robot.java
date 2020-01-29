package org.frcteam753.c2020;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.command.Scheduler;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import org.frcteam753.c2020.autonomous.AutonomousSelector;
import org.frcteam753.c2020.autonomous.AutonomousTrajectories;
import org.frcteam753.c2020.subsystems.*;
import org.frcteam753.c2020.vision.api.Gamepiece;
import org.frcteam753.common.robot.drivers.NavX;
import org.frcteam753.common.robot.subsystems.SubsystemManager;
import org.frcteam753.c2020.RobotMap

public class Robot extends TimedRobot {
    private static final double UPDATE_DT = 5e-3; // 5 ms
    private  AnalogInput Fl_enc = new AnalogInput(RobotMap.DRIVETRAIN_FRONT_LEFT_ANGLE_ENCODER);
    private  AnalogInput Fr_enc = new AnalogInput(RobotMap.DRIVETRAIN_FRONT_RIGHT_ANGLE_ENCODER);
    private  AnalogInput Rl_enc = new AnalogInput(RobotMap.DRIVETRAIN_BACK_LEFT_ANGLE_ENCODER);
    private  AnalogInput Rr_enc = new AnalogInput(RobotMap.DRIVETRAIN_BACK_RIGHT_ANGLE_ENCODER);
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
        System.out.println("Fl encoder at "+ Fl_enc )
        System.out.println("Fr encoder at "+ Fr_enc)
        System.out.println("Rl encoder at "+ Rl_enc)
        System.out.println("Rr encoder at "+ Rr_enc)
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
