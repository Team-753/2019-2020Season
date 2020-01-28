package org.frcteam2910.c2019;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.GenericHID;
import edu.wpi.first.wpilibj.command.*;
import edu.wpi.first.wpilibj.shuffleboard.Shuffleboard;
import edu.wpi.first.wpilibj.shuffleboard.ShuffleboardTab;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import org.frcteam753.c2020.autonomous.AutonomousSelector;
import org.frcteam753.c2020.commands.*;
import org.frcteam753.c2020.subsystems.*;
import org.frcteam753.common.robot.commands.ZeroFieldOrientedCommand;


public class OI {
    Joystick myOnlyJoy = new Joystick(0);
    

    public OI() {
        primaryController.getLeftXAxis().setInverted(true);
        primaryController.getRightXAxis().setInverted(true);

        primaryController.getRightXAxis().setScale(0.45);
    }

    public void bindButtons(AutonomousSelector autonomousSelector) {
        

}

